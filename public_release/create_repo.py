import os
import subprocess
from contextlib import contextmanager
from public_release.initial_files import generate_setup_py_text, setup_sh_text, setup_cfg_text, dot_gitignore_text, \
    readme_template, get_requirements_text
from public_release.module_mover import copy_modules_to_dir


def fill_repo_with_initial_files(
        package_name,
        destination_dir,
        root_package = None,
        author=None,
        author_email=None,
        long_description=None,
        version=0,
        install_requires=(),
        dependency_links = (),
        repo_dependencies = (),
        scripts=[],
        commit_and_push = False,
        ):

    setup_file_txt = generate_setup_py_text(
        name=package_name,
        author=author,
        author_email=author_email,
        long_description=long_description,
        version=version,
        install_requires=install_requires,
        dependency_links=dependency_links,
        scripts=scripts
        )

    with open(os.path.join(destination_dir, 'setup.py'), 'w') as f:
        f.write(setup_file_txt)

    with open(os.path.join(destination_dir, 'setup.sh'), 'w') as f:
        f.write(setup_sh_text)

    with open(os.path.join(destination_dir, 'setup.cfg'), 'w') as f:
        f.write(setup_cfg_text)

    with open(os.path.join(destination_dir, '.gitignore'), 'w') as f:
        f.write(dot_gitignore_text)

    readme_file = os.path.join(destination_dir, 'README.md')
    is_git_repo = subprocess.call('git status', shell=True)==0
    if is_git_repo:
        git_url = subprocess.check_output('git config --get remote.origin.url', shell=True)
        if not os.path.exists(readme_file):
            with current_directory(destination_dir):
                repo_name = subprocess.check_output('basename `git rev-parse --show-toplevel`', shell=True)
                with open(readme_file, 'w') as f:
                    f.write(readme_template.format(name=package_name, git_url=git_url, repo_name=repo_name, ))

        if commit_and_push:
            subprocess.call('git add .', shell=True)
            subprocess.call('git commit -m "added initial files"', shell=True)
            subprocess.call('git push -u origin master', shell=True)

    if root_package is not None:
        try:
            os.makedirs(os.path.join(destination_dir, root_package))
        except OSError:
            pass
        with open(os.path.join(destination_dir, '__init__.py'), 'w') as f:
            f.write('')

    with open(os.path.join(destination_dir, 'requirements.txt'), 'w') as f:
        f.write(get_requirements_text(repo_dependencies))


def create_git_repo(local_folder, repo_url, add_all = True):

    try:
        os.makedirs(local_folder)
    except OSError:
        pass

    with current_directory(local_folder):
        subprocess.call('git init', shell=True)
        if add_all:
            subprocess.call('git add .', shell=True)
        subprocess.call('git commit -m "first commit"', shell=True)
        subprocess.call('git remote add origin {}'.format(repo_url), shell=True)
        subprocess.call('git push -u origin master', shell=True)


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
        long_description=None,
        version=0,
        install_requires=(),
        dependency_links = (),
        repo_dependencies = (),
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

    fill_repo_with_initial_files(
        package_name=package_name,
        root_package = root_package,
        destination_dir=destination_dir,
        author=author,
        author_email=author_email,
        long_description=long_description,
        version=version,
        install_requires=install_requires,
        dependency_links=dependency_links,
        repo_dependencies=repo_dependencies,
        scripts=scripts
        )


@contextmanager
def current_directory(path):
    oldpath = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(oldpath)


if __name__ == '__main__':
    copy_and_create_setup('artemis.plotting.demo_dbplot', '/Users/peter/projects/tests/artemistest5', root_package='dbplot_demo', package_name='artemis_demo', clear_old_package=True)
