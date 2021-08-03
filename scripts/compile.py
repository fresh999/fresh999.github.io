#!/usr/bin/env python

import argparse
import markdown
import numpy as np

thm_envs = ['theorem', 'proposition', 'lemma', 'proof']
math_envs = ['equation', 'align']
list_envs = ['enumerate']

# block is a list of strings
def is_math_block(block):
    for line in block:
        for env in math_envs:
            if f'\\begin{{{env}' in line:
                return True
    return False

# block is a list of strings
def find_thm_type(chunk):
    for line in chunk:
        for env in thm_envs:
            if f'\\begin{{{env}}}' in line:
                return env
    return None

class Block:
    # lines is a list of strings
    def __init__(self, lines, is_math=False):
        self.lines = lines
        self.is_math = is_math

    def insert_tags(self):
        if self.is_math:
            self.lines.insert(0, '<p>\n')
            self.lines.append('</p>\n')
        else:
            self.lines = ['<p>' + line.rstrip() + '</p>\n' if not line == '\n' else line for line in self.lines]

class PostChunk:
    def __init__(self, lines, thm_type=None):
        self.lines = lines
        self.thm_type = thm_type

    def find_math_envs(self):
        beg = []
        end = []
        for i, line in enumerate(self.lines):
            for env in math_envs:
                if f'\\begin{{{env}' in line:
                    beg.append(i)
                if f'\\end{{{env}' in line:
                    end.append(i+1)
        return [i for tup in zip(beg, end) for i in tup]

    def parse_chunk(self):
        indices = self.find_math_envs()
        blocks = [sl.tolist() for sl in np.split(self.lines, indices)]
        self.blocks = [Block(block, is_math_block(block)) for block in blocks]

    def insert_tags(self):
        if self.thm_type:
            for block in self.blocks[1:-2]:
                block.insert_tags()
        for block in self.blocks:
            block.insert_tags()

    def delimit_chunk(self):
        if self.thm_type:
            for line in self.blocks[0].lines:
                if f'\\begin{{{self.thm_type}}}' in line:
                    self.blocks[0].lines.remove(line)
            for line in self.blocks[-1].lines:
                if f'\\end{{{self.thm_type}}}' in line:
                    self.blocks[-1].lines.remove(line)
            self.blocks.append(Block(['</div>\n']))
            self.blocks.insert(0, Block([f'<div class="{self.thm_type}">\n']))

    def compile_chunk(self):
        blocks = self.parse_chunk()
        self.insert_tags()
        self.delimit_chunk()

class Post:
    def __init__(self, post_filename):
        with open(post_filename, 'r') as post:
            self.lines = post.readlines()

    def get_beg_end_indices(self):
        beg_ix = 0
        end_ix = 0
        for i, line in enumerate(self.lines):
            if '\\begin{document}' in line:
                beg_idx = i+1
            if '\\end{document}' in line:
                end_idx = i
        return (beg_idx, end_idx)

    def get_post_lines(self):
        beg_ix, end_ix = self.get_beg_end_indices()
        self.lines = self.lines[beg_ix : end_ix]
#        this gets rid of blank lines
#        self.lines = [line for line in self.lines if line.strip()]

    def find_thm_envs(self):
        beg = []
        end = []
        for i, line in enumerate(self.lines):
            for env in thm_envs:
                if f'\\begin{{{env}}}' in line:
                    beg.append(i)
                if f'\\end{{{env}}}' in line:
                    end.append(i+1)
        return [i for tup in zip(beg, end) for i in tup]

    def parse_post(self):
        indices = self.find_thm_envs()
        chunks = [sl.tolist() for sl in np.split(self.lines, indices)]
        return [PostChunk(chunk, find_thm_type(chunk)) for chunk in chunks]

    def compile_post(self):
        self.get_post_lines()
        chunks = self.parse_post()
        for chunk in chunks:
            chunk.compile_chunk()
        blocks = [block for chunk in chunks for block in chunk.blocks]
        return blocks

class MarkdownCompiler:
    def __init__(self, post_filename):
        with open(post_filename, 'r') as post:
            self.md_content = post.read()
            self.html_content = markdown.markdown(self.md_content, extensions=['fenced_code', 'attr_list'])

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compiles blog post written in LaTeX or Markdown')
    parser.add_argument('--input', type=str, default=None, help='The source code for the blog post')

    args = parser.parse_args()
    if not args.input:
        print('No input file provided')
        exit(0)

#    post = Post(args.input)
#    blocks = post.compile_post()
#    pars = [line for block in blocks for line in block.lines]
#    print(''.join(pars))

    md_compiler = MarkdownCompiler(args.input)
    print(md_compiler.html_content)

