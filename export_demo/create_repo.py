from setuptools import setup
from export_demo import copy_modules_to_dir

_arg_order = 'name', 'author', 'author_email', 'url', 'long_description', 'version', 'packages'




def generate_setup_file(**kwargs):

    txt = 'from setuptools import setup'
    txt+= '\n\nsetup('
    sorted_qwargs = [(_arg_order[k], kwargs[_arg_order[k]]) for k in _arg_order if k in kwargs]+[(k, v) for k, v in kwargs.iteritems() if k not in _arg_order]
    for name, val in sorted_qwargs:
        txt += '\n    {} = {},'.format(name, val)
    txt+= '\n    )'
    return txt


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
        )

