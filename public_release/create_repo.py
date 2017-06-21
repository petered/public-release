import os
import subprocess
from contextlib import contextmanager
from public_release.initial_files import generate_setup_py_text, setup_sh_text, setup_cfg_text, dot_gitignore_text, \
    readme_template, get_requirements_text
from public_release.module_mover import copy_modules_to_dir
from ast import parse


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

            readme_file = 'README.md'
            if not os.path.exists(readme_file):
                with current_directory(destination_dir):
                    repo_name = subprocess.check_output('basename `git rev-parse --show-toplevel`', shell=True).replace('\n', '')
                    pip_install_url = github_url_to_pip_install_url(github_url)
                    with open(readme_file, 'w') as f:
                        f.write(readme_template.format(name=package_name, git_url=github_url, repo_name=repo_name, pip_url=pip_install_url))

            if commit_and_push:
                subprocess.call('git add .', shell=True)
                subprocess.call('git commit -m "added initial files"', shell=True)
                subprocess.call('git push -u origin master', shell=True)


def get_github_url(user_or_org, repo_name):
    return 'https://github.com/{user}/{name}.git'.format(user=user_or_org, name=repo_name)


def github_url_to_repo_name(github_url):
    return os.path.splitext(os.path.split(github_url)[1])[0]


def github_url_to_pip_install_url(github_url):
    return 'git+'+github_url+'#egg='+github_url_to_repo_name(github_url)


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

    github_response = subprocess.check_output('curl -u \'{user}\' https://api.github.com/repos/{user}/{repo}'.format(user=user, repo=repo_name), shell=True)
    # repo_exists = "Not Found" not in
    repo_does_not_exist = "Not Found" in github_response
    repo_exists = repo_name in github_response

    # From: https://stackoverflow.com/a/23916276/851699

    if repo_exists:
        if if_existing=='ok':
            print 'Repo {} already exists.  Proceeding...'.format(github_url)
        elif if_existing=='check':
            print
            import time; time.sleep(0.01)
            response = raw_input('Repo {} already exists.  Proceed anyway with existing repo?  (y, n) >>'.format(github_url))
            assert response in ('y', 'n')
            if response!='y':
                raise Exception('Repo {} already exists'.format(github_url))
        elif if_existing=='error':
            raise Exception('Repo {} already exists'.format(github_url))
    elif repo_does_not_exist:
        # From https://stackoverflow.com/a/10325316/851699
        repo_making_output = subprocess.check_output('curl -u \'{user}\' {api_path} -d \'{{"name":"{repo}", "private":{private}}}\''.format(user=user, api_path=api_path, repo=repo_name, private='true' if private else 'false'), shell=True)
        if repo_name not in repo_making_output:
            raise Exception('Repo Creation seems to have failed: {}'.format(repo_making_output))
    else:
        raise Exception('Got response from GitHub: {}'.format(github_response))
    return github_url


def print_repo_info(git_url, local_path):
    repo_name = github_url_to_repo_name(git_url)
    pip_path = github_url_to_pip_install_url(git_url)
    print '='*15 + ' SUCCESS! ' + '='*15
    print 'Created the repo: {}'.format(git_url)
    print 'It exists locally at {}'.format(local_path)
    print 'You can set up the repo with: \n  $ cd {}; source setup.sh'.format(local_path)
    print 'Our you can install the repo as source in your current environment with: \n  $ pip install -e {}'.format(pip_path)
    print 'A new user can install your repo with: \n  $ git clone {}; cd {}; source setup.sh'.format(git_url, repo_name)
    print '='*40


def is_valid_variable_name(name):
    # Thank you mhawke: https://stackoverflow.com/a/36331242/851699
    try:
        parse('{} = None'.format(name))
        return True
    except (SyntaxError, ValueError, TypeError):
        return False


def create_public_release(
        github_user,
        repo_name,
        modules = None,
        root_package=None,
        scope = 'project',
        destination_dir=None,
        private=False,
        organization=None,
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

    github_url=create_github_repo(
        user=github_user,
        repo_name=repo_name,
        private=private,
        org_name=organization,
        if_existing='ok'
        )

    if destination_dir is None:
        destination_dir = os.path.join(os.path.expanduser("~"), 'projects', repo_name)

    if root_package is None:
        root_package = repo_name.replace('-', '_')
    assert is_valid_variable_name(root_package)

    if modules is not None:
        copy_modules_to_dir(
            object=modules,
            destination_dir=destination_dir,
            root_package=root_package,
            clear_old_package=clear_old_package,
            code_subpackage=code_subpackage,
            helper_subpackage=helper_subpackage,
            scope=scope,
            )

    fill_repo_with_initial_files(
        package_name=repo_name,
        root_package = root_package,
        destination_dir=destination_dir,
        author=author,
        author_email=author_email,
        long_description=long_description,
        version=version,
        install_requires=install_requires,
        dependency_links=dependency_links,
        repo_dependencies=repo_dependencies,
        scripts=scripts,
        github_url=github_url,
        commit_and_push=True
        )

    print_repo_info(git_url=github_url, local_path=destination_dir)


@contextmanager
def current_directory(path):
    oldpath = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(oldpath)


if __name__ == '__main__':
    create_public_release('artemis.plotting.demo_dbplot', '/Users/peter/projects/tests/artemistest5', root_package='dbplot_demo', clear_old_package=True)
