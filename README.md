# Public Release
A small utility for exporting a script, along with all its dependencies, into a new repo in your code

This tool is useful if you have a demo script in you own code that you want to rease to the public, and you do not want to release your entire code-base because of confidentiality or the fact that your code is an embarassing mess.

Using this tool, you can select the script you want to run, collect all modules upon which your script depends, and move them to a self-contained demo repo.  

## To install public-release

In bash, within your current python environment, go:

```
pip install -e git+http://github.com/petered/public-release.git#egg=public-release
```

## To Create a Public Release:

Suppose we want to make a public release of a project `spiking-experiments` that of the code required to generate all figures in a paper.  `spiking-experiments` is large repository with a lot of irrelevant stuff.  We have one function in this repo that we want to release to the public.

![](https://github.com/petered/data/raw/master/images/Screen%20Shot%202017-06-13%20at%204.31.12%20PM.png)

Now, create the repository that you'd like to release on github (We'll call it `pdnn`):

![](https://github.com/petered/data/raw/master/images/Screen%20Shot%202017-06-13%20at%204.40.23%20PM.png)

Clone your new repository onto your computer, and copy the local path that the repo is stored in:

Now, from within the environment of `spiking-experiments`, install `public-release` (see installation instructions above).  You can then run, the following code to fill yout new repository with the release code (`spiking_experiments.dynamic_networks.figures`) and all required code, along with the setup code, which installs all dependencies (note that you need to copy the local path `/Users/peter/projects/pdnn` to your new repo).

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

Now, after verifying that everything works, commit you code:

```
cd ~/projects/pdnn
git add *
git commit -am 'first release'
git push
```

That's it, your code is released.

## For others to install and run your code

Now, for others to install and run the code from your public release, they can just clone your repo, and run the setup script.

```
git clone https://github.com/petered/pdnn.git
cd pdnn
source setup.sh
```
... Which will install the code and dependencies.  (Note that these instructions are automatically added to the README.md of your new repository).  If everything installs without error, they can run the module of interest:

```
python pdnn/figures.py
```

