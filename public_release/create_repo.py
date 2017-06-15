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
        github_url = None,
        commit_and_push = True
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

    try:
        os.makedirs(destination_dir)
    except OSError:
        pass

    with current_directory(destination_dir):
        with open('setup.py', 'w') as f:
            f.write(setup_file_txt)

        with open('setup.sh', 'w') as f:
            f.write(setup_sh_text)

        with open('setup.cfg', 'w') as f:
            f.write(setup_cfg_text)

        with open('.gitignore', 'w') as f:
            f.write(dot_gitignore_text)

        readme_file = 'README.md'

        if root_package is not None:
            try:
                os.makedirs(os.path.join(destination_dir, root_package))
            except OSError:
                pass
            with open(os.path.join(destination_dir, root_package, '__init__.py'), 'w') as f:
                f.write('')

        with open(os.path.join(destination_dir, 'requirements.txt'), 'w') as f:
            f.write(get_requirements_text(repo_dependencies))

        if github_url is not None:
            is_git_repo = subprocess.call('git status', shell=True)==0
            if is_git_repo:
                remote_url = subprocess.check_output('git config --get remote.origin.url', shell=True).replace('\n', '')
                assert remote_url==github_url, "This repository already has a remote url: {}, which doesn't match the github url you listed: {}".format(remote_url, github_url)
            else:
                # From: https://stackoverflow.com/a/16811212/851699
                subprocess.call('git init .', shell=True)
                subprocess.call('git remote add -t \* -f origin {}'.format(github_url), shell=True)
                subprocess.call('git checkout master', shell=True)

            if not os.path.exists(readme_file):
                with current_directory(destination_dir):
                    repo_name = subprocess.check_output('basename `git rev-parse --show-toplevel`', shell=True).replace('\n', '')
                    with open(readme_file, 'w') as f:
                        f.write(readme_template.format(name=package_name, git_url=github_url, repo_name=repo_name, ))

            if commit_and_push:
                subprocess.call('git add .', shell=True)
                subprocess.call('git commit -m "added initial files"', shell=True)
                subprocess.call('git push -u origin master', shell=True)


def get_github_url(user_or_org, repo_name):
    return 'https://github.com/{user}/{name}.git'.format(user=user_or_org, name=repo_name)


def get_pip_install_path(user_or_org, repo_name):
    return 'git+http://github.com/{user_or_org}/{repo}.git#egg={repo}'.format(user_or_org=user_or_org, repo=repo_name)


def create_github_repo(user, repo_name, private=False, org_name=None, if_existing='ok'):

    assert private in (True, False)
    assert if_existing in ('ok', 'check', 'error')
    if org_name is None:
        org_name=user

    # Check if it already exists
    github_url = get_github_url(user_or_org=org_name, repo_name=repo_name)
    api_path = 'https://api.github.com/user/repos' if user==org_name else 'https://api.github.com/orgs/{org}/repos'.format(org=org_name)
    repo_exists = "Not Found" not in subprocess.check_output('curl {api_path}'.format(api_path=api_path), shell=True)
    # From: https://stackoverflow.com/a/23916276/851699

    if repo_exists:
        if if_existing=='ok':
            pass
        elif if_existing=='check':
            print
            import time; time.sleep(0.01)
            response = raw_input('Repo {} already exists.  Proceed anyway with existing repo?  (y, n) >>'.format(github_url))
            assert response in ('y', 'n')
            if response!='y':
                raise Exception('Repo {} already exists'.format(github_url))
        elif if_existing=='error':
            raise Exception('Repo {} already exists'.format(github_url))
    else:
        # From https://stackoverflow.com/a/10325316/851699
        subprocess.call('curl -u \'{user}\' {api_path} -d \'{{"name":"{repo}", "private":"{private}"}}\''.format(user=user, api_path=api_path, repo=repo_name, private='true' if private else 'false'), shell=True)
    return github_url


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
