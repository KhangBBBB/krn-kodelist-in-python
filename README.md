# KRUN
A system supporting literate programming, meta programming, and reproducible research for Troff.

# Introduction
This project contains a set of preprocessors/processors to support literate programming, metaprogramming, and reproducible research for Troff typesetting system.
Users can use these preprocessor on any plain text file (using their own macro package, etc) as long as the syntax are according to kdoc/kodelist.

The project was initially a small project I submitted for Python class and also to support me to manage note/code easier in programming classes/projects.
I do hope others also find it useful.

What makes kodelist and krun effective is that they are made as simple filters to be used with other utilities and standard tools and.
Its ability to desmontrating a demonstration in a document comes in handy.
Users can utilize these tools effortlessly with any text editor, IDE, or in the terminal on their phone without drastically change in workflow when switching different editing environment unlike most interactive tools.
Operation of krun and kodelist are all stream manipulation, therefore, users' source documents are unaffected.
With proper techniques, users can add these programs to their workflow for daily note-taking, specific file management, data science and software development.

kodelist and krun are written in Python programming language and currently using only Python standard modules.
The programs should work on all machines that have Python interpreter.
kodelist and krun are still in their early development stage, therefore, Python seems to be a good choice to choose for quick prototying.
Later on, KRUN and KODELIST are likely to be ported to C for speed and archiving.

# Directory Explain:

* krun: project folder
    * src: containing source folder
        * krun: folder containing source code of krun program
        * kodelist: folder containing source code of kodelist program
    * doc: containg program manual folder
        * krun: containg krun program manual
        * kodelist: containg kodelist program manual
    * README.md
    * Makefile
    * LICENSE

# User Manual:
* Inside doc directory


# Installation
## Dependency
* There is no special dependency for the programs beside Python interpreter and Python standard library.

## Linux users:
* Run:

        sudo make all && make install

* Clean up:

        make clean


# Example:
## Example 1:

* File: file

        .TOFILE python test1.py
        .HEAD 1 "Python programming"
        .PP
        Variable:
        .CODES python test1.py pass123
        x = 1
        y = 2
        .CODEE pass123
        .PP
        Print statement:
        .CODES python test1.py
        print("Result is", x + y)
        .CODEE
        .RUN python test1.py
        .EVALUATE python test1.py

* To run the code snippet and get output from standard output:

        cat file | krun -r


* To typeset this document with result from code evaluation (using Heirloom Troff backend engine):

        cat file | krun -e | kodelist | eqn | pic | tbl | troff -mkdoc -x |  dpost | ps2pdf - file.pdf

* To typeset this document with result from code evaluation (using Groff backend engine):

        cat file | krun -e | kodelist | groff -mkdoc -k -e -t -p -g -Tps | ps2pdf - file.pdf

* Note
    * Make sure users install kdoc macro package to use or write their own include macros from krun/kodelist.
    * Using -help option for more information about usage.

            krun -help
            kodelist -help


# Bug Report:
* There is no major bug found.


# About
* Author: Khang Bao
* Version: 0.4
* Since: March 13, 2021
