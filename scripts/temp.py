#!/usr/bin/env python

import numpy as np
import re

opening_p = re.compile(r'^\s*\\begin\{.*\}')
closing_p = re.compile(r'^\s*\\end\{.*\}')

list_envs = ['enumerate']
math_envs = ['equation', 'align']
thm_envs = ['theorem', 'proposition', 'lemma', 'proof']

def get_outer_subblocks(lines):
    indices = []
    env_count = 0
    for i, line in enumerate(lines):
        match = opening_p.match(line)
        if match:
            env_count += 1
            if env_count == 1:
                indices.append(i)
        elif closing_p.match(line):
            env_count -= 1
            if env_count == 0:
                indices.append(i+1)
    blocks = [sl.tolist() for sl in np.split(lines, indices)]
    blocks = list(filter(([]).__ne__, blocks))
    return [Block(b) for b in blocks]

def get_post_lines(lines):
    start = 0
    end = 0
    for i, line in enumerate(lines):
        if re.search(r'^\s*\\begin\{document\}', line):
            start = i+1
        if re.search(r'^\s*\\end\{document\}', line):
            end = i
    return lines[start : end]

class Block:
    def __init__(self, lines):
        self.lines = lines

    def get_block_type(self):
        if not self.lines:
            return None
        pattern = re.compile(r'^\s*\\begin\{(.*)\}')
        m = pattern.match(self.lines[0])
        if m:
            self.lines = self.lines[1:-1]
            return m.group(1)

    def process_block(self):
        subblocks = get_outer_subblocks(self.lines)
        self.type = self.get_block_type()
        if len(subblocks) == 1:
            self.insert_tags()
            return self.lines
        return [line for block in subblocks for line in block.process_block()]

    def insert_tags(self):
        if not self.type:
            self.lines = ['<p>' + line.rstrip() + '</p>\n' for line in self.lines if not re.search(r'^\s*\n$', line)]
        elif self.type in thm_envs:
            self.lines.insert(0, f'<div class="{self.type}">\n')
            self.lines.append('</div>\n')
        elif self.type in list_envs:
            self.lines.insert(0, '<ol>\n')
            self.lines.append('</ol>\n')
            self.lines = [re.sub(r'\\item\s(.*)$', r'<li>\1</li>', line) for line in self.lines]


class Post(Block):
    def __init__(self, post_filename):
        with open(post_filename, 'r') as post:
            lines = post.readlines()
            super().__init__(get_post_lines(lines))


if __name__ == '__main__':

    post = Post('../latex_posts/art.tex')
#    print(''.join(post.lines))

    print(''.join(post.process_block()))

    l = [1, 2, 3, 4, 5]
    ids = [0, 5]
    lol = [sl.tolist() for sl in np.split(l, ids) if sl.any()]
    print(lol)

