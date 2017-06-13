# Public Release
A small utility for exporting a script, along with all its dependencies, into a new repo in your code

This tool is useful if you have a demo script in you own code that you want to rease to the public, and you do not want to release your entire code-base because of confidentiality or the fact that your code is an embarassing mess.

Using this tool, you can select the script you want to run, search for all dependencies within your current repo, and move them to a self-contained demo repo.

## To install

`pip install -e git+http://github.com/petered/public-release.git#egg=public-release`

## Example:

Suppose we want to make a public release that of the code required to generate all figures in a paper.  We have a large repository, and one function in this repo that we want to release to the public.

![](https://github.com/petered/data/raw/master/images/Screen%20Shot%202017-06-13%20at%204.31.12%20PM.png)

