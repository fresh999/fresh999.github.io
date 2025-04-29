#!/usr/bin/env python

import argparse
import markdown
import os

class Template:
    def __init__(self, templ_filename):
        self.hook = '<!-- Hook -->'
        self.title_hook = '<!-- Title hook -->'
        with open(templ_filename, 'r') as templ:
            self.lines = templ.read().splitlines()

    def find_hooks(self):
        for i, line in enumerate(self.lines):
            if self.hook in line:
                return i

class MarkdownCompiler:
    def __init__(self, post_filename):
        with open(post_filename, 'r') as post:
            self.md_content = post.read()
            md = markdown.Markdown(extensions=['fenced_code', 'attr_list', 'meta', 'smarty'])
            self.html_content = md.convert(self.md_content).splitlines()
            self.meta = md.Meta

    def compile_template(self, template):
        hook_idx = template.find_hooks()
        if not hook_idx:
            return self.html_content
        title = '<h1>' + self.meta['title'][0] + '</h1>'
        return template.lines[:hook_idx] + [title] + self.html_content + template.lines[hook_idx + 1:]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compiles blog post written in Markdown')
    parser.add_argument('--output-dir', type=str, default='../posts', help='The directory that stores the posts')
    parser.add_argument('--input', type=str, default=None, help='The source code for the blog post')

    args = parser.parse_args()
    if not args.input:
        print('No input file provided')
        exit(0)

    md_compiler = MarkdownCompiler(args.input)
    template = Template('../templates/post.html')
    post_lines = md_compiler.compile_template(template)

    basename = os.path.splitext(os.path.basename(args.input))[0]
    with open(os.path.join(args.output_dir, basename + '.html'), 'w') as post:
        post.write('\n'.join(post_lines))
