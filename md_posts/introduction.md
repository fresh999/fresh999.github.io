Title: Welcome to my blog!
Summary: Introduction to the blog.
Authors: Fresh
Date: August 5, 2021


This is the first post on FreshBlog. As such, it is going to be an introduction to the origin, the purpose and the future developments of the blog.

FreshBlog grew out of my desire to get into web development, together with the fact that it is the ideal place for me to share and discuss what I do on a daily basis, which goes from maths and physics to tinkering with software. The philosophy that underpins this project is that of minimalism, from the graphical side to the actual code that powers the blog. So, I decided to ditch all static site generators and just write some HTML and CSS myself.

I only had two fundamental needs for the blog: it had to have LaTeX support (for maths and physics) and it should display source code blocks in a clean and readable way. I took care of the first point by using [MathJax](https://www.mathjax.org), which is very nice and popular ([Wikipedia](https://www.wikipedia.org) also uses it). The second need is less straightforward. HTML supports code blocks but it is also quite cumbersome, especially for LaTeX enthusiasts like me. So the question was: how do I write my posts? Do I just grind out raw HTML or do I use something else? In the end, I decided to go with [Markdown](https://daringfireball.net/projects/markdown/), as it makes for very readable text.
I used the `python-markdown`{class=prettyprint} Python module. Here is some of the code I wrote:

``` {class=prettyprint}
class MarkdownCompiler:
    def __init__(self, post_filename):
        with open(post_filename, 'r') as post:
            self.md_content = post.read()
            md = markdown.Markdown(extensions=['fenced_code', 'attr_list', 'meta'])
            self.html_content = md.convert(self.md_content).splitlines()
            self.meta = md.Meta

    def compile_template(self, template):
        hook_idx = template.find_hooks()
        if not hook_idx:
            return self.html_content
        title = '<h1>' + self.meta['title'][0] + '</h1>'
        return template.lines[:hook_idx] + [title] + self.html_content + template.lines[hook_idx + 1:]
```

Basically, this reads the Markdown post, converts it to HTML and uses a template to compile the final HTML blog post. I have also made use of some extensions of `python-markdown`{class=prettyprint}, which you can read all about at [Extensions](https://python-markdown.github.io/extensions/).

Now, Markdown does support LaTeX, but I really like my LaTeX setup and I would like to be able to use LaTeX when writing blog posts strictly about maths or physics. This is why I am currently working on a LaTeX to HTML compiler, which I am going to blog about.

There are many more projects on my to-do list and I am only going to reveal a couple. First, I would like to style the blog using animations. Second, I want to add a comments section.

There you go! I am excited to launch the blog and I am looking forward to finishing the setup process. Stay fresh!




