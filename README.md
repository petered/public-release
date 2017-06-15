# Public Release
A small utility for exporting a script, along with all its dependencies, into a new repo in your code

This tool is useful if you have a demo script in you own code that you want to rease to the public, and you do not want to release your entire code-base because of confidentiality or the fact that your code is an embarassing mess.

Using this tool, you can select the script you want to release, collect all modules upon which your script depends, and move them to a self-contained demo repo.  

## To install public-release

In bash, within your current python environment, go:

```
pip install -e git+http://github.com/petered/public-release.git#egg=public-release
```

## To Create a Public Release:

Suppose we want to make a public release of a project `spiking-experiments` that of the code required to generate all figures in a paper.  `spiking-experiments` is large repository with a lot of irrelevant stuff.  We have one function in this repo that we want to release to the public.

![](https://github.com/petered/data/raw/master/images/Screen%20Shot%202017-06-13%20at%204.31.12%20PM.png)

From within the environment of `spiking-experiments`, install `public-release` (see installation instructions above).  You can then run the following code to fill yout new repository with the release code (`spiking_experiments.dynamic_networks.figures`) and all required code, along with the setup code, which installs all dependencies (note that you need to copy the local path `/Users/peter/projects/pdnn` to your new repo).

```
from public_release.create_repo import create_public_release


create_public_release(
    github_user='petered',
    repo_name='pdnn',
    private=False,
    modules = 'spiking_experiments.dynamic_networks.figures',
    clear_old_package=True,
    author="Peter O'Connor",
    author_email='poconn4@gmail.com',
    install_requires = ['numpy', 'matplotlib', 'theano', 'scipy'],
    repo_dependencies = [
        '-e git+http://github.com/QUVA-Lab/artemis.git@1.4.1#egg=artemis',
        '-e git+http://github.com/petered/plato.git@0.2.0#egg=plato',
        ]
    )

```

The code will ask for your github password in order to create a new repository.  If all is successful, you will get the message:

```
=============== SUCCESS! ===============
Created the repo: https://github.com/petered/pdnn.git
It exists locally at /Users/peter/projects/pdnn
You can set up the repo with: 
  $ cd /Users/peter/projects/pdnn; source setup.sh
Our you can install the repo as source in your current environment with: 
  $ pip install -e git+http://github.com/petered/pdnn.git#egg=pdnn
A new user can install your repo with: 
  $ git clone https://github.com/petered/pdnn.git; cd pdnn; source setup.sh
========================================
```

That's it, your code is released.
