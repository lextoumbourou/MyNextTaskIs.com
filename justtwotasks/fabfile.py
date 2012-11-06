import os

from fabric.api import run, env, settings, cd, put, sudo
from fabric.contrib import files

import private


def prod():
    env.hosts = list(private.PROD_SERVERS)


def local():
    env.hosts = ['localhost']


def deploy():
    """Update the repository"""
    # Create the repo if it doesn't already exist
    git_repo = 'git://github.com/lextoumbourou/justtwotasks.com.git'
    with settings(warn_only=True):
        if run('test -d {0}'.format(private.APP_DIR)).failed:
            run('git clone {0} {1}'.format(git_repo, private.APP_DIR))
    # Ensure I own the directory
    sudo("chown -R {0} {1}".format(private.USER_GROUP, private.APP_DIR))
    # Django app deployment tasks 
    with cd(private.APP_DIR):
        run('git pull')
        put('private.py', 'private.py')
        run('python ../manage.py syncdb')
        run('python ../manage.py collectstatic  --noinput')
        run('python ../manage.py compress --force')
        run('touch apache/django.wsgi')

def compile():
    """Compile less code and install JS components"""
    pass


def update_bootstrap(tag=None):
    """
    Updates Bootstrap files to tag version. If a tag isn't specified,
    just get latest version.
    """
    repo = 'https://github.com/twitter/bootstrap'
    with settings(warn_only=True):
        # Delete Bootstrap from the tmp location
        if not files.exists('~/src'):
            print "File doesn't exist"
            run('mkdir ~/src')
        if not files.exists('~/src/bootstrap'):
            run('cd ~/src/; git clone {0}'.format(repo))

        with cd('~/src/bootstrap/'):
            run('git pull origin master') 
            if tag:
                run('git checkout {0}'.format(tag))
            local_path = os.path.join(os.path.dirname(__file__), 'templates/static/less/bootstrap')
            run('cp -fR less {0}'.format(local_path))
