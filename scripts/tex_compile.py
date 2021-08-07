#!/usr/bin/env python

import numpy as np
import re

opening_p = re.compile(r'^\s*\\begin\{.*\}')
closing_p = re.compile(r'^\s*\\end\{.*\}')

def find_outer_blocks(lines):
    indices = []
    env_count = 0
    for i, line in enumerate(lines):
        if opening_p.match(line):
            env_count += 1
            if env_count == 1:
                indices.append(i)
        elif closing_p.match(line):
            env_count -= 1
            if env_count == 0:
                indices.append(i+1)
    return indices

def get_post_lines(lines):
    start = 0
    end = 0
    for i, line in enumerate(lines):
        if re.search(r'^\\begin\{document\}', line):
            start = i+1
        if re.search(r'^\\end\{document\}', line):
            end = i
    return lines[start : end]

class Block:
    def __init__(self, lines):
        self.lines = lines
        self.type = self.get_block_type()

    def get_subblocks(self):
        indices = find_outer_blocks(self.lines)
        blocks = [sl.tolist() for sl in np.split(self.lines, indices)]
        return [Block(b) for b in blocks]

    def get_block_type(self):
        if not self.lines:
            return None
        pattern = re.compile(r'^\s*\\begin\{(.*)\}')
        m = pattern.match(self.lines[0])
        if m:
            return m.group(1)

class Post(Block):
    def __init__(self, post_filename):
        with open(post_filename, 'r') as post:
            lines = post.readlines()
            super().__init__(get_post_lines(lines))


if __name__ == '__main__':

    post = Post('../latex_posts/article.tex')
    print(''.join(post.lines))

    blocks = post.get_subblocks()
    for b in blocks:
        print(b.type)

