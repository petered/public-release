from importlib import import_module
from modulefinder import ModuleFinder
import inspect
import os
from shutil import rmtree
import logging
logging.basicConfig()
LOGGER = logging.getLogger('export-demo')
LOGGER.setLevel(logging.INFO)


def get_src_file(module):
    return module.__file__[:-1] if module.__file__.endswith('.pyc') else module.__file__


def get_module_import_dict(object, just_own_package = True, remove_packages = True):
    """
    Given some code object (or the full name of a module), find all the modules that must be imported for this object to
    run.
    :param object:
    :param just_own_package:
    :return:
    """
    if isinstance(object, (list, tuple)):
        dicts, names = zip(*[get_module_import_dict(ob, just_own_package=just_own_package) for ob in object])
        return {k: v for d in dicts for k, v in d.iteritems()}, names
    elif isinstance(object, basestring):
        module = import_module(object)
    else:
        module = inspect.getmodule(object)
    module_file = get_src_file(module)
    finder = ModuleFinder()
    this_package = module.__name__.split('.')[0]
    LOGGER.info('Scanning Dependent Modules in {}.  This may take some time...'.format(this_package))
    finder.run_script(module_file)
    if just_own_package:
        modules = {name: mod for name, mod in finder.modules.iteritems() if name.split('.')[0]==this_package}
    else:
        modules = finder.modules
    LOGGER.info('Scan Complete.  {} dependent modules found.'.format(len(modules)))
    modules[module.__name__] = module  # Don't forget yourself!
    module_name_to_module_path = {name: get_src_file(m) for name, m in modules.iteritems()}
    if remove_packages:
        module_name_to_module_path = {name: path for name, path in module_name_to_module_path.iteritems() if not (path.endswith('__init__.py') or path.endswith('__init__.pyc'))}
    return module_name_to_module_path, module.__name__


def copy_modules_to_dir(object, destination_dir, root_package, code_subpackage=None, helper_subpackage ='helpers', clear_old_package = False):

    modules, names = get_module_import_dict(object, just_own_package=True)
    if isinstance(names, basestring):
        names = [names]
    root_dir = os.path.join(destination_dir, root_package)

    if clear_old_package and os.path.exists(root_dir):
        rmtree(root_dir)

    code_dir = root_dir if code_subpackage is None else os.path.join(root_dir, code_subpackage)
    code_module_name = root_package if code_subpackage is None else root_package+'.'+code_subpackage
    helper_module_name = root_package if helper_subpackage is None else root_package+'.'+helper_subpackage

    helper_dir = root_dir if helper_subpackage is None else os.path.join(root_dir, helper_subpackage)

    for direct in (root_dir, code_dir, helper_dir):
        try:
            os.makedirs(direct)
        except OSError:
            pass
        with open(os.path.join(direct, '__init__.py'), 'w') as f:
            f.write('')

    old_name_to_new_name = {module_name: code_module_name+'.'+module_name.split('.')[-1] if module_name in names else helper_module_name+'.'+module_name.split('.')[-1] for module_name in modules.keys()}
    old_name_to_new_path = {module_name: os.path.join(code_dir, os.path.split(module_file)[1]) if module_name in names else os.path.join(helper_dir, os.path.split(module_file)[1]) for module_name, module_file in modules.iteritems()}

    for module_name, module_path in modules.iteritems():
        _, file_name = os.path.split(module_path)

        with open(module_path) as f:
            txt = f.read()

        for dep_module_name, new_module_name in old_name_to_new_name.iteritems():
            txt = txt.replace('from {} import '.format(dep_module_name), 'from {} import '.format(new_module_name))
            txt = txt.replace('import {}'.format(dep_module_name), 'import {}'.format(new_module_name))

        with open(old_name_to_new_path[module_name], 'w') as f:
            f.write(txt)

        LOGGER.info('Copied {} -> {}'.format(module_path, old_name_to_new_path[module_name]))


if __name__ == '__main__':
    copy_modules_to_dir('artemis.plotting.demo_dbplot', '/Users/peter/projects/tests/artemistest5', root_package='dbplot_demo', clear_old_package=True)
