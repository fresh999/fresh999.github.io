Title: FreshParse - LaTeX for the Web
Summary: Description of the LaTeX to HTML compiler FreshParse
Authors: Fresh
Date: August 22, 2021

Hi everyone and welcome back to a brand new post! Today we are going to be looking at FreshParse, a lightweight LaTeX to HTML compiler I just wrote. Let's dive right in!

This project grew out of my love of LaTeX and my desire to use it on FreshBlog. The goal was to build a program that would insert paragraph tags, process mathematical environments and handle lists. Nothing too fancy.

I knew nothing about compilers before starting out and my original approach was not successful. Basically, I was trying to process LaTeX code by identifying the outermost environments and then recursively analyzing the content of said environments. This approach made heavy use of regular expressions and I got stuck pretty quickly, as I could not get nested environments to work. Then I found out that compilers use *syntax-directed translation* and that I should write a lexer and a parser. At that point I was doubtful that I would ever see this through, as I knew nothing about parsing. I was stuck.

Watching a [Brian Kernighan](https://en.wikipedia.org/wiki/Brian_Kernighan) video in which he explained the origins of the [AWK](https://en.wikipedia.org/wiki/AWK) programming language, I found out about [Lex](https://en.wikipedia.org/wiki/Lex_(software)) and [Yacc](https://en.wikipedia.org/wiki/Yacc), Unix tools that are used to write compilers and that Kernighan had used himself to implement AWK. My project suddenly had renewed hope and in three or four days I got a first running version of the compiler.

Lex works by detecting regular expressions and performing actions accordingly. Although it can be used on its own, it excels when used together with Yacc. Basically, Lex generates a stream of tokens for Yacc to parse. The combination of the two tools is so powerful that you could write a fully-fledged C compiler with it! I will not delve too much into Lex, but I will briefly discuss Yacc.

Yacc takes a *grammar* and executes snippets of C code whenever a rule is recognized. This is a small part of the Yacc code for FreshParse:

``` {class=prettyprint}
thm_env: thm env_content end_thm_like
       | prop env_content end_thm_like
       | lemma env_content end_thm_like
       | proof env_content end_thm_like
       | definition env_content end_thm_like
       ;

items: env {print_indentation(indent_level); printf("</li>\n");}
     | item
     | items env {print_indentation(indent_level); printf("</li>\n");}
     | items item
     ;
```

The first rule defines a theorem-like environment (the vertical bar `|` is a logical or). No C code is executed in this case. The second rule, instead, specifies what the content of a list should look like. First of all, note that this time C code is executed. Secondly, and more importantly, the second is rule is *recursive*. This is a very powerful mechanism that perfectly matches the idea of nested environments, which is ubiquitous in programming languages.

FreshParse wraps sentences into `<p>` tags. As far as mathematics is concerned, it wraps theorems in `<div>` tags together with a `class` attribute, which is useful for CSS styling. For instance,

```
\begin{lemma}
    Suppose a non-empty partially ordered set P has the property that every non-empty chain has an upper bound in P. Then the set P contains at least one maximal element.
\end{lemma}
```
get translated to

``` {class=prettyprint}
<div class="lemma">
    Suppose a non-empty partially ordered set P has the property that every non-empty chain has an upper bound in P. Then the set P contains at least one maximal element.
 </div>
```

Also, it recognizes displayed math environments, such as `\begin{equation}` and does not alter them, as [MathJax](https://www.mathjax.org) is capable of rendering them. Finally, it can process lists by wrapping them in `<ol>` (or `<ul>`) tags.

The code for FreshParse is available at [fresh999/FreshParse](https://github.com/fresh999/FreshParse). You are welcome to check it out and play with it. Comments and feedback are also highly appreciated!

That's it for this one, folks! Till next time, stay fresh!


