Title: Vim and LaTeX - A match made in heaven
Summary: A quick overview of my typesetting setup
Authors: Fresh
Date: February 9, 2021


Hi everyone and welcome back to a brand new post! Today, we are going to take a look at how to configure Vim and setup a LaTeX typesetting workstation.

First of all, what is Vim? It's the most genius (I'm getting deliberately controversial here) text editor ever invented. Its whole phylosophy revolves around the idea that one shouldn't have to move its hands away from the keyboard while typing (it makes sense, right?) and it achieves this by introducing different user modes and viewing keys both as characters and as commands, or actions, according to the mode the user is in. It is also highly configurable and it supports external plug-ins. Lastly, and perhaps most importantly, Vim has its own programming language, called Vimscript, and there lies its true power. The only drawback is its learning curve, which is a bit steeper than mainstream text editors. However, the possibilities Vim unlocks largely outweigh any initial hurdles and you'll find yourself unable to revert to anything you were used to after trying it.

Let's now see how Vim can turn your LaTeX typesetting on its head.

Ideally, we would like typeset our code, compile it in place and have it displayed in real time, much like the [Overleaf](https://www.overleaf.com/) experience. The problem with Overleaf is two-fold. Firstly, the typing-compiling process is not seamless, as you have to click to compile the document. Secondly, it forces you to work online and to rely on external resources, while it's possible (and highly desirable if you ask me) to store everything locally and just work on your machine.

Here is my solution.
First, I set up auto-compilation in my ```.vimrc```, which is the main place where you do your Vim customization. This is done by just adding the following lines of code:

~~~
function! Bin()
    let s:bin_path = Head() . '/bin'
    if !isdirectory(s:bin_path)
        call mkdir(s:bin_path)
    endif
endfunction

" Compiling LaTeX document
    nnoremap <leader>c :<C-u> w <bar> call Bin() <bar> ! pdflatex -output-directory="bin" -synctex=1 -interaction=nonstopmode %:p <cr><cr>
~~~

This remaps the sequence `<leader>c` in *normal mode* to the command that compiles the document. Here, `<leader>` is any key you want (I have it mapped to my space bar). So, all you need to do to compile your LaTeX document is to go into normal mode and press that sequence of keys. You can play a similar trick with bibliography compilation:

~~~
" Compiling bibliography
    nnoremap <leader>b :<C-u>! biber --output-directory=bin %:.:r<cr><cr>
~~~

To preview the pdf document, we need a pdf reader. I use Zathura, a Vim-like (I wonder why I like it), modular pdf reader that supports auto-refresh and `synctex`. Then, add the following line of code:

~~~
" Previewing pdf document
nnoremap <leader>p :<C-u>! zathura bin/%:.:r.pdf & disown<cr><cr>
~~~

So, `<leader>b` will compile your bibliography and `<leader>p` will display the document. Since Zathura supports auto-refresh, you don't need to hit `<leader>p` every time you want to see the pdf. Simply recompiling will be enough.

What about those nice drop-down menus with auto-completion suggestions that Overleaf offers? This is where snippet engines come into play. I use [UltiSnips](https://github.com/sirver/UltiSnips), an amazing Vim plug-in that allows you to define your custom snippets for any filetype. Just to give you a taste of what UltiSnips offers, here is one the snippets I use most often:

~~~
snippet beg "Generic environment" b
\begin{$1}
	${2:<++>}
\end{$1}
endsnippet
~~~

Suppose you want to insert a list into your LaTeX document. Then, you have to open the `itemize` enviroment, write your list and then close it:

~~~
\begin{itemize}
    \item First item
    \item Second item
\end{itemize}
~~~

Everyone knows how annoying and repetitive this can get. The above snippet allows you to simply type `beg` and hit `Tab` to trigger the expansion of the snippet:

~~~
\begin{|}
    <++>
\end{}
~~~

The cursor will automatically end up inside the first set of curly brackets and whatever you type there will automatically also appear in the second set of brackets. Then, with one more `Tab` hit, the cursor will jump in between the two enviroment delimiters, delete the placeholder `<++>` and switch to insert mode. Once you are done with your list items, one last `Tab` hit will take you outside the `itemize` enviroment. Notice that not once have you had the need of reaching for your mouse!

Obviously, the customization of Vim doesn't stop here, but I will leave it to your creativity to find new ways of exploiting Vim's features. Enjoy your LaTeX document preparation. Until next time, stay fresh!















