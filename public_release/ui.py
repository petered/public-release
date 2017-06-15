import getpass
import os
from ast import parse
from public_release.create_repo import fill_repo_with_initial_files, get_github_url, create_github_repo, \
    get_pip_install_path


def get_user_response(prompt, default = None):
    if default is not None:
        prompt += ' [{}]'.format(default)
    prompt += ' >>'
    user_input = raw_input(prompt)
    stripped = user_input.lstrip(' ').rstrip(' ')
    if stripped=='':
        if default is None:
            raise Exception('Error: You provided no response and no default was given.')
        else:
            return default
    else:
        return stripped


def is_valid_variable_name(name):
    # Thank you mhawke: https://stackoverflow.com/a/36331242/851699
    try:
        parse('{} = None'.format(name))
        return True
    except (SyntaxError, ValueError, TypeError):
        return False


def ui_initialize_repo():

    print 'This will take you through initializing a repository.  Options in [square brackets] are defaults.'

    # Github setup questions
    name = get_user_response('Enter Repo Name')
    assert ' ' not in name
    github_user = get_user_response('Enter GitHub username')
    github_org = get_user_response('Enter GitHub user/organization to create repo in', default=github_user)
    is_private = get_user_response('Make Repo Private? (y/n)', default='n')
    assert is_private in ('y', 'n')

    root_name = get_user_response('Enter Name of root code package', default=name.replace('-', '_'))
    assert is_valid_variable_name(root_name)
    local_path = get_user_response('Enter Local Path for repo', default=os.path.join(os.path.expanduser("~"), 'projects', name))
    author = get_user_response('Author', default=getpass.getuser())
    dependencies = [d.lstrip(' ').rstrip(' ') for d in get_user_response('List Comma-Separated Dependencies (eg "numpy,scipy")', default='').split(',')]

    is_private = is_private=='y'

    git_url = get_github_url(user_or_org=github_org, repo_name=name)

    response = get_user_response('Ready to create the following repo:\n' +
         '  git url: {}\n'.format(git_url) +
         '  Root Package Name: {}\n'.format(root_name) +
         '  Local Path: {}\n'.format(local_path) +
         '  Author: {}\n'.format(author) +
         '  Dependencies: {}\n'.format(dependencies) +
         '  Private?: {}\n'.format('Yes' if is_private else 'No'),
         'Confirm Decision? (y/n)'
         )

    if response!='y':
        print 'Cancelled.'
        return

    git_url = create_github_repo(
        user=github_user,
        repo_name=name,
        private=is_private,
        org_name=github_org,
        if_existing='check'
        )

    fill_repo_with_initial_files(
        package_name=name,
        destination_dir=local_path,
        root_package=root_name,
        author=author,
        install_requires=dependencies,
        github_url=git_url,
        commit_and_push=True,
        )

    print '='*15 + ' SUCCESS! ' + '='*15
    print 'Created the repo: {}'.format(git_url)
    print 'It exists locally at {}'.format(local_path)
    print 'You can set up the repo with: \n  $ cd {}; source setup.sh'.format(local_path)
    print 'Our you can install the repo as source in your current environment with: \n  $ pip install -e {}'.format(get_pip_install_path(user_or_org=github_org, repo_name=name))
    print 'A new user can install your repo with: \n  $ git clone {}; cd {}; source setup.sh'.format(git_url, name)
    print '='*40

if __name__ == '__main__':
    ui_initialize_repo()
