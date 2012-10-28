from fabric.api import run, env, settings, cd, put, sudo

import private


def prod():
    env.hosts = list(private.PROD_SERVERS)


def deploy():
    """Update the repository"""
    # Create the repo if it doesn't already exist
    git_repo = 'git://github.com/lextoumbourou/justtwotasks.com.git'
    with settings(warn_only=True):
        if run('test -d {0}'.format(private.APP_DIR)).failed:
            run('git clone {0} {1}'.format(git_repo, private.APP_DIR))
    # Ensure I own the directory
    sudo("chown -R " + private.USER_GROUP + " " + private.APP_DIR)
    # Django app deployment tasks 
    with cd(private.APP_DIR):
        run('git pull')
        put('private.py', 'private.py')
        run('python ../manage.py syncdb')
        run('python ../manage.py collectstatic  --noinput')
        run('touch apache/django.wsgi')
