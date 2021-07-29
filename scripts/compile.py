#!/usr/bin/env python

class Post:
    def __init__(self):
        self.post_paragraphs = []

    def read_post(self, post_filename):
        with open(post_filename, 'r') as post:
            self.lines = post.readlines()

if __name__ == '__main__':

    post = Post()
    post.read_post('../latex_posts/mathematical_induction.tex')
    for line in post.lines:
        print(line)

