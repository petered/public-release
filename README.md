# Public Release
A small utility for exporting a script, along with all its dependencies, into a new repo in your code

This tool is useful if you have a demo script in you own code that you want to rease to the public, and you do not want to release your entire code-base because of confidentiality or the fact that your code is an embarassing mess.

Using this tool, you can select the script you want to release, collect all modules upon which your script depends, and create a repository on GitHub that others can easily use to install and run your code.

1. [Installing public-release](#installing-public-release)
2. [Create a Public Release](#create-a-public-release)
3. [Create a new repo from scratch](#create-a-new-repo-from-scratch)

## Installing public-release

In bash, within your current python environment, go:

```
pip install -e git+http://github.com/petered/public-release.git#egg=public-release
```

## Create a Public Release:

Suppose we want to make a public release of a project `spiking-experiments` that of the code required to generate all figures in a paper.  `spiking-experiments` is large repository with a lot of irrelevant stuff.  We have one function in this repo that we want to release to the public.

![](https://github.com/petered/data/blob/master/images/Screen%20Shot%202017-06-15%20at%203.35.48%20PM.png)

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

That's it, your code is released.  If you look at your new repository, you will see that it has been populated by the function `figures.py`, which you wanted to release, along with all modules on which it depends:

![](https://github.com/petered/data/blob/master/images/Screen%20Shot%202017-06-15%20at%203.09.18%20PM.png)


## Create a new repo from scratch

After installing public release, you can You can run 

```
python -c "from public_release.ui import ui_initialize_repo; ui_initialize_repo"
```

This will take you into a UI for creating a new repo which can easily be installed with pip later on.  First you're taken through a series of questions:

![](https://github.com/petered/data/blob/master/images/Screen%20Shot%202017-06-15%20at%203.12.58%20PM.png)

And then, after some setup:

![](https://github.com/petered/data/blob/master/images/Screen%20Shot%202017-06-15%20at%203.13.31%20PM.png)


