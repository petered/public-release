from public_release.create_repo import create_public_release


def test_create_public_release():
    # Note this is not good to run as an actual unittest because it requires that the user enter their password.
    create_public_release(
        github_user='petered',
        repo_name='my_test_repo',
        private=False,
        modules = None,
        clear_old_package=True,
        author="Peter O'Connor",
        author_email='poconn4@gmail.com',
        install_requires = ['numpy'],
        repo_dependencies = [
            '-e git+http://github.com/QUVA-Lab/artemis.git@1.4.1#egg=artemis',
            ]
        )

if __name__ == '__main__':
    test_create_public_release()
