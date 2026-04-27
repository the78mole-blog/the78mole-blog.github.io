---
title: Doxygen - Tips and Tricks
date: '2020-05-28'
description: ''
categories:
- Tools
- Uncategorized
tags:
- doxygen
---

## LaTeX non-interactive

To make LaTeX skip some errors without user interaction, you can add the option `--interaction=nonstopmode` to the pdflatex call. Easiest way to do so, is changing the LATEX\_COMMAND\_NAME in your Doxyfile.

LATEX\_CMD\_NAME = "latex --interaction=nonstopmode"

Do not forget the double quotation marks. Otherwise doxygen will remove the space and the command in your make.bat will fail.

If you now want to generate the code, step into your doxygen-generated latex folder (designated by `LATEX_OUTPUT` option in Doxyfile) and execute `make.bat` (on Windows) or `make all` (on \*nix).

## Adding a favicon to html output

Adding a favicon to html output, you need to specify it in a custom header and include the original image in HTML, as described [here](https://stackoverflow.com/questions/18215463/how-to-set-a-favicon-for-doxygen-output). To extract the default header file:

```
doxygen -w html headerFile
```

Add the follwing line to in headerFile within the html header

```
<link rel="shortcut icon" href="favicon.png" type="image/png">
```

And add your headerFile and the image to the HTML\_EXTRA\_FILES in your Doxyfile. Its path is relative to your Doxyfile.

```
HTML_HEADER = headerFile
HTML_EXTRA_FILES = some_rel_path/favicon.png
```

Now you can generate your html documentation with some favicon in place.

## PDF output destination

Did you ever search for the PDF file, doxygen (or better the Makefile in latex) generates? I just added an option to doxygen, copying the refman.pdf to a location of your choice. (Hopefully it soon get's merged and released).

If you want to test it out? Compile doxygen from [my doxygen fork](https://github.com/the78mole/doxygen) and add the following option to the Doxyfile of your project.

PDF\_DST\_FILE = ../MyGenerated.pdf

The destination is relative to your Makefile in your doxygen latex folder. As soon as make finished it's job, the PDF is just in the same folder, the latex folder resides in.

That's all. Enjoy generating software documentation with doxygen
