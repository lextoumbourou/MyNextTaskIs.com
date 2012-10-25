from fabric.api import run, env, settings, cd

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
    # Perform Git pull and update time stamp of wsgi file for Apache
    with cd(private.APP_DIR):
        run('git pull')
        run('touch apache/django.wsgi')
