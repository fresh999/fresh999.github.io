#!/usr/bin/env python

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
                    end.append(i)
        return list(zip(beg, end))

    def get_post_blocks(self):
        envs = self.find_math_envs()
        math_blocks = []
        reg_blocks = []
        for i, (beg, end) in enumerate(envs):
            math_blocks.append(Block(self.lines[beg : end+1], True))
            if i == 0:
                reg_blocks.append(Block(self.lines[:beg]))
            else:
                reg_blocks.append(Block(self.lines[envs[i-1][1] + 1 : beg]))
        if envs[-1][1] != len(self.lines) - 1:
            reg_blocks.append(Block(self.lines[envs[-1][1] + 1:]))
        blocks = []
        i = 0
        while i < len(math_blocks):
            blocks.append(reg_blocks[i])
            blocks.append(math_blocks[i])
            i += 1
        if len(reg_blocks) > len(math_blocks):
            blocks.append(reg_blocks[-1])
        return blocks

    def insert_tags(self, blocks):
        for block in blocks:
            block.insert_tags()
        return blocks

    def parser(self):
        math_openers = ['\\begin{equation', '\\begin{align']
        math_closers = ['\\end{equation', '\\end{align']
        blocks = []
        switch = False
        i = 0
        while i < len(self.lines):
            for o in math_openers:
                if o in self.lines[i]:
                    for c in math_closers:
                        while c not in self.lines[i]:
                            i += 1

    def compile_post(self):
        self.get_post_lines()
        blocks = self.get_post_blocks()
        return self.insert_tags(blocks)

#    def find_thm_envs(self):
#        thm_openers = ['\\begin{theorem}', '\\begin{proposition}', '\\begin{lemma}']
#        thm_closers = ['\\end{equation}', '\\end{proposition}' '\\end{lemma}']
#        beg = []
#        end = []
#        for i, line in enumerate(self.lines):
#            for o in thm_openers:
#                if o in line:
#                    beg.append(i)
#            for c in thm_closers:
#                if c in line:
#                    end.append(i)
#        return zip(beg, end)


if __name__ == '__main__':

    post = Post('../latex_posts/mathematical_induction.tex')
    blocks = post.compile_post()


    pars = [line for block in blocks for line in block.lines]
    print(''.join(pars))

#    for block in post.math_blocks:
#        print(block.lines)
#    for block in post.blocks:
#        print(block.lines)

#    print(post.lines)
#    print(''.join(post.lines))


