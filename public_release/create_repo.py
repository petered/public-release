from public_release.module_mover import copy_modules_to_dir
import os
_arg_order = 'name', 'author', 'author_email', 'url', 'long_description', 'version', 'packages'


def generate_setup_file_text(**kwargs):
    txt = 'from setuptools import setup, find_packages'
    txt+= '\n\nsetup('
    sorted_qwargs = [(k, kwargs[k]) for k in _arg_order if k in kwargs]+[(k, v) for k, v in kwargs.iteritems() if k not in _arg_order]
    for name, val in sorted_qwargs:
        if val is not None:
            txt += '\n    {} = {},'.format(name, '"'+val+'"' if isinstance(val, basestring) else str(val))
    txt+= '\n    packages=find_packages(),'
    txt+= '\n    )\n'
    return txt


setup_text="""virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .
"""

def copy_and_create_setup(
        modules,
        destination_dir,
        root_package,
        package_name,
        code_subpackage=None,
        helper_subpackage ='helpers',
        clear_old_package = False,
        author=None,
        author_email=None,
        # url='https://github.com/QUVA-Lab/spiking-mlp',
        long_description=None,
        version=0,
        dependencies=(),
        scripts=[],
        ):

    copy_modules_to_dir(
        object=modules,
        destination_dir=destination_dir,
        root_package=root_package,
        clear_old_package=clear_old_package,
        code_subpackage=code_subpackage,
        helper_subpackage=helper_subpackage,
        )

    setup_file_txt = generate_setup_file_text(
        name=package_name,
        author=author,
        author_email=author_email,
        long_description=long_description,
        version=version,
        dependencies=dependencies,
        scripts=scripts
        )

    with open(os.path.join(destination_dir, 'setup.py'), 'w') as f:
        f.write(setup_file_txt)

    with open(os.path.join(destination_dir, 'setup.sh'), 'w') as f:
        f.write(setup_text)


if __name__ == '__main__':
    copy_and_create_setup('artemis.plotting.demo_dbplot', '/Users/peter/projects/tests/artemistest5', root_package='dbplot_demo', package_name='artemis_demo', clear_old_package=True)
