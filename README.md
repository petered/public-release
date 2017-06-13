# Public Release
A small utility for exporting a script, along with all its dependencies, into a new repo in your code

This tool is useful if you have a demo script in you own code that you want to rease to the public, and you do not want to release your entire code-base because of confidentiality or the fact that your code is an embarassing mess.

Using this tool, you can select the script you want to run, search for all dependencies within your current repo, and move them to a self-contained demo repo.

## To install

`pip install -e git+http://github.com/petered/public-release.git#egg=public-release`

## Example:

Suppose we want to make a public release of a project `spiking-experiments` that of the code required to generate all figures in a paper.  `spiking-experiments` is large repository with a lot of irrelevant stuff.  We have one function in this repo that we want to release to the public.

![](https://github.com/petered/data/raw/master/images/Screen%20Shot%202017-06-13%20at%204.31.12%20PM.png)

Now, create the repository that you'd like to release on github (We'll call it `pdnn`):

![](https://github.com/petered/data/raw/master/images/Screen%20Shot%202017-06-13%20at%204.40.23%20PM.png)

Clone your new repository onto your computer, and copy the local path that the repo is stored in:

Now, from within the environment if `spiking-experiments`, install `public-release` (see installation instructions above).  You can then run, the following code to fill yout new repository with the release code, along with the setup code, which installs all dependencies (note that you need to copy the local path to your new repo).

```
from public_release.create_repo import copy_and_create_setup


copy_and_create_setup(
    modules = 'spiking_experiments.dynamic_networks.figures',
    destination_dir='/Users/peter/projects/pdnn',
    root_package='pdnn',
    package_name='pdnn',
    clear_old_package=True,
    author="Peter O'Connor",
    author_email='poconn4@gmail.com',
    install_requires = ['numpy', 'matplotlib', 'theano', 'scipy'],
    repo_dependencies = [
        '-e git+http://github.com/QUVA-Lab/artemis.git#egg=artemis',
        '-e git+http://github.com/petered/plato.git#egg=plato',
        ]
    )
```

Now you will see that your new repo is populated by the demo-function, along with all modules on which it depends:

![](https://github.com/petered/data/raw/master/images/Screen%20Shot%202017-06-13%20at%204.33.28%20PM.png)
