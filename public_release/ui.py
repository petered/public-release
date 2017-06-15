import getpass
import os
from public_release.create_repo import fill_repo_with_initial_files, get_github_url, create_github_repo, \
    get_pip_install_path, print_repo_info, is_valid_variable_name


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


def ui_initialize_repo():

    print 'This will take you through initializing a repository.  Options in [square brackets] are defaults.'

    # Github setup questions
    name = get_user_response('Enter Repo Name')
    assert ' ' not in name
    github_user = get_user_response('Enter GitHub username')
    github_user_or_org = get_user_response('Enter GitHub user/organization to create repo in', default=github_user)
    is_private = get_user_response('Make Repo Private? (y/n)', default='n')
    assert is_private in ('y', 'n')

    root_name = get_user_response('Enter Name of root code package', default=name.replace('-', '_'))
    assert is_valid_variable_name(root_name)
    local_path = get_user_response('Enter Local Path for repo', default=os.path.join(os.path.expanduser("~"), 'projects', name))
    author = get_user_response('Author', default=getpass.getuser())
    dependencies = [d.lstrip(' ').rstrip(' ') for d in get_user_response('List Comma-Separated Dependencies (eg "numpy,scipy")', default='').split(',')]

    is_private = is_private=='y'

    git_url = get_github_url(user_or_org=github_user_or_org, repo_name=name)

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
        org_name=github_user_or_org,
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

    print_repo_info(git_url=git_url, local_path=local_path, repo_name=name, github_user_or_org=github_user_or_org)

if __name__ == '__main__':
    ui_initialize_repo()
