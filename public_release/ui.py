import getpass
import os

from public_release.create_repo import fill_repo_with_initial_files, create_git_repo


def get_user_response(prompt, default = None):
    if default is not None:
        prompt += ' [{}]'.format(default)
    prompt += '>>'
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

    name = get_user_response('Enter Repo Name')
    assert ' ' not in name

    root_name = get_user_response('Enter Name of root code package', default=name.replace('-', '_'))
    assert ' ' not in root_name

    local_path = get_user_response('Enter Local Path for repo', default=os.path.join(os.path.expanduser("~"), 'projects', name))
    author = get_user_response('Author', default=getpass.getuser())
    dependencies = [d.lstrip(' ').rstrip(' ') for d in get_user_response('List Comma-Separated Dependencies (eg "numpy,scipy")', default='').split(',')]

    git_user = get_user_response('Enter GitHub username/organization: ')

    git_url = 'https://github.com/{user}/{name}.git'.format(user=git_user, name=name)

    response = get_user_response('Ready to create the following repo:\n' +
         '  Root Package Name: {}\n'.format(root_name) +
         '  Local Path: {}\n'.format(local_path) +
         '  Author: {}\n'.format(author) +
         '  Dependencies: {}\n'.format(dependencies) +
         '  git url: {}\n'.format(git_url) +
         'Confirm Decision? (y/n)'
         )

    if response!='y':
        print 'Cancelled.'
        return

    create_git_repo(local_folder=local_path, repo_url=git_url)

    fill_repo_with_initial_files(
        package_name=name,
        destination_dir=local_path,
        root_package=root_name,
        author=author,
        install_requires=dependencies,
        commit_and_push=True,
        )

    print 'Created the repo: <a href="{url}">{url}</a>'.format(url=git_url)

if __name__ == '__main__':
    ui_initialize_repo()
