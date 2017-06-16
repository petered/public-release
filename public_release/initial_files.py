

def generate_setup_py_text(**kwargs):
    """
    Return the text for a setup.py file.
    :param kwargs:
    :return:
    """
    _arg_order = 'name', 'author', 'author_email', 'url', 'long_description', 'version', 'packages'
    txt = 'from setuptools import setup, find_packages'
    txt+= '\n\nsetup('
    sorted_qwargs = [(k, kwargs[k]) for k in _arg_order if k in kwargs]+[(k, v) for k, v in kwargs.iteritems() if k not in _arg_order]
    for name, val in sorted_qwargs:
        if val is not None:
            txt += '\n    {} = {},'.format(name, '"'+val+'"' if isinstance(val, basestring) else str(val))
    txt+= '\n    packages=find_packages(),'
    txt+= '\n    )\n'
    return txt


readme_template= """
# {name}

To set up this repo, go:

```
git clone {git_url}
cd {repo_name}
source setup.sh
```

Or to be able to import this code in an existing Python environment, go:

```
pip install -e {pip_url}
```

> This repo has been auto-generated by the [Public Release Package](https://github.com/petered/public-release)
"""


setup_sh_text= """virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
"""

setup_cfg_text = """[pytest]
norecursedirs = venv
"""


def get_requirements_text(repo_dependencies):
    """
    :param repo_dependencies: A list of git repositories.  You can optionall add pip arguments such as '-e' (install as source).
        e.g.: ['-e git+http://github.com/QUVA-Lab/artemis.git#egg=artemis', '-e git+http://github.com/petered/plato.git#egg=plato']
    :return: The text of the requirements.txt file.
    """
    if len(repo_dependencies)==0:
        return '.\n'
    else:
        return '\n'.join(repo_dependencies)


dot_gitignore_text = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# dotenv
.env

# virtualenv
.venv
venv/
ENV/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# PyCharm settings
.idea

# mkdocs documentation
/site

# mypy
.mypy_cache/
"""