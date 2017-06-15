# Public Release
A small utility for exporting a python script, along with all its dependencies, into a new GitHub repository, so that it can easily be installed and run by other people.

This tool is useful if you have a demo script that you want to rease to the public, but you do not want to release your entire code-base because of confidentiality or the fact that your code is an embarassing mess.

1. [Installing public-release](#installing-public-release)
2. [Create a Public Release](#create-a-public-release)
3. [Create a new repo from scratch](#create-a-new-repo-from-scratch)

## Installing public-release

In terminal, within the python environment of your current project, go:

```
pip install -e git+http://github.com/petered/public-release.git#egg=public-release
```

## Create a Public Release:

Suppose we want to make a public release of a function `figures.py`, which generates all the figures in a paper.  `figures.py` lives in a large project `spiking-experiments` (and depends on several modules in this project), which also includes a lot of irrelevant stuff that we don't want to release.

![](https://github.com/petered/data/blob/master/images/Screen%20Shot%202017-06-15%20at%203.35.48%20PM.png)

From within the environment of `spiking-experiments`, install `public-release` (see installation instructions above).  You can then run the following code:

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
(Obviously replace "petered" with your own GitHub user name, and changing the other fields as appropriate for your project).

When run, this code will ask for your github password in order to create a new repository.  It fills your new repository with the release code (`spiking_experiments.dynamic_networks.figures`) and all modules on which it depends.  It also creates setup code (`setup.sh`, `setup.py`, etc), which lets people easily install all dependencies required to make this repo run.

If all is successful, you will get the message:

![](https://github.com/petered/data/blob/master/images/Screen%20Shot%202017-06-15%20at%204.33.07%20PM.png)

That's it, your code is released.  If you look at your [new repository](https://github.com/petered/pdnn), you will see that it has been populated by the function `figures.py`, which you wanted to release, along with all modules on which it depends:

![](https://github.com/petered/data/blob/master/images/Screen%20Shot%202017-06-15%20at%203.09.18%20PM.png)


## Create a new repo from scratch

public-release also lets you create a new git repo from scratch, and fills it with the basic files (setup.py, requirements.txt, .gitignore, README.md, etc), so that it can be easily pip-installed by other users.  

After installing `public-release`, you can run 

```
python -c "from public_release.ui import ui_initialize_repo; ui_initialize_repo()"
```

This will take you into a UI for creating a new repo which can easily be installed with pip later on.  First you're taken through a series of questions:

![](https://github.com/petered/data/blob/master/images/Screen%20Shot%202017-06-15%20at%203.12.58%20PM.png)

And then, after some setup:

![](https://github.com/petered/data/blob/master/images/Screen%20Shot%202017-06-15%20at%203.13.31%20PM.png)


