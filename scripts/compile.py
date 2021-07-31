#!/usr/bin/env python

import numpy as np

# block is a list of strings
def is_math_block(block):
    math_openers = ['\\begin{equation', '\\begin{align']
    for line in block:
        for o in math_openers:
            if o in line:
                return True
    return False

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

class Post:
    def __init__(self, post_filename):
        with open(post_filename, 'r') as post:
            self.lines = post.readlines()

    def get_beg_end_indices(self):
        beg_ix = 0
        end_ix = 0
        for i, line in enumerate(self.lines):
            if line == '\\begin{document}\n':
                beg_idx = i+1
            if line == '\\end{document}\n':
                end_idx = i
        return (beg_idx, end_idx)

    def get_post_lines(self):
        beg_ix, end_ix = self.get_beg_end_indices()
        self.lines = self.lines[beg_ix : end_ix]
        while '\n' in self.lines:
            self.lines.remove('\n')

    def find_math_envs(self):
        math_openers = ['\\begin{equation', '\\begin{align']
        math_closers = ['\\end{equation', '\\end{align']
        beg = []
        end = []
        for i, line in enumerate(self.lines):
            for o in math_openers:
                if o in line:
                    beg.append(i)
            for c in math_closers:
                if c in line:
                    end.append(i+1)
        return [i for tup in zip(beg, end) for i in tup]

    def parse_post(self):
        indices = self.find_math_envs()
        blocks = [sl.tolist() for sl in np.split(self.lines, indices)]
        return [Block(block, is_math_block(block)) for block in blocks]

    def insert_tags(self, blocks):
        for block in blocks:
            block.insert_tags()
        return blocks

    def compile_post(self):
        self.get_post_lines()
        blocks = self.parse_post()
        return self.insert_tags(blocks)

    def find_thm_envs(self):
        thm_openers = ['\\begin{theorem}', '\\begin{proposition}', '\\begin{lemma}']
        thm_closers = ['\\end{equation}', '\\end{proposition}' '\\end{lemma}']
        beg = []
        end = []
        for i, line in enumerate(self.lines):
            for o in thm_openers:
                if o in line:
                    beg.append(i)
            for c in thm_closers:
                if c in line:
                    end.append(i)
        return zip(beg, end)


if __name__ == '__main__':

    post = Post('../latex_posts/mathematical_induction.tex')
    blocks = post.compile_post()

    pars = [line for block in blocks for line in block.lines]
    print(''.join(pars))

#    print(post.lines)
#    print(''.join(post.lines))


