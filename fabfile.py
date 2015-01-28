from fabric.api import *
from cuisine import *
from deploy.fab.virtualenv import *
from deploy.fab.django import *
from deploy.fab.nginx import * 
from deploy.fab.git import *
from deploy.fab.gunicorn import * 
from deploy.fab.pillow import *
from deploy.fab.memcached import *
from deploy.fab.solr import *
from deploy.fab.mongo import *
from uuid import uuid4
import os
import deploy.fab

 # change from the default user to 'vagrant'
env.venv_path = '.venv'
env.project_name = "pipfix"
env.project_domain = "www.pipfix.com"
env.project_path = '.'
env.project_config_template = 'deploy/conf/local.prod.py'
env.project_config_path = 'server/conf/local.py'
env.project_local_media_path = "media"
env.project_remote_media_path = "media"
env.project_local_db_path = 'db.sqlite3'
env.requirements_path = 'deploy/requirements.txt'
env.config_template = 'deploy/conf/settings.template.py'
env.config = 'settings.py'
env.gunicorn_template = 'deploy/conf/gunicorn.conf.py'
env.gunicorn_config = 'gunicorn.py'
env.nginx_template = 'deploy/conf/nginx.conf'
env.supervisor_template = 'deploy/conf/supervisor.conf'

env.db_name = 'pipfix'
env.db_username = 'pipfix_user'
env.db_password = str(uuid4()) 
env.djangokey = str(uuid4())

@task
def deploy():
    mongodb_ensure() 
    git_ensure(env.project_path)
    virtualenv_ensure(env.project_path, env.venv_path, env.requirements_path)
    postgresql_ensure(
        env.db_name,
        env.db_username,
        env.project_path,
        env.db_password,
        env.venv_path
    )
    django_ensure(
        env.project_path,
        env.project_name,
        env.project_config_template,
        env.project_config_path,
        env,
        env.venv_path
    )
    gunicorn_ensure(
        env.project_path,
        env.project_name, 
        env.gunicorn_template,
        env.gunicorn_config,
        env.supervisor_template,
        env,
        env.venv_path
    )
    nginx_ensure(
        env.project_path,
        env.project_name, 
        env.nginx_template,
        env
    )

@task
def rebuild_index():
    django_search_ensure(
        env.project_path,
        env.venv_path
    )

@task
def create_superuser():
    django_create_superuser(
        env.project_path,
        env.venv_path
    )

@task
def status():
    sudo("supervisorctl status %s" % env.project_name)

@task
def pulldata():
    django_replace_data(
        env.project_path,
        env.project_local_db_path, 
        env.project_local_media_path,
        env.project_remote_media_path,
        env.venv_path)

@task
def backup():
    django_backup(
        env.project_path,
        env.project_remote_media_path,
        env.venv_path
    )

@task
def prod():
    """ Set demo hosts """
    env.user = 'mativs'
    env.hosts = ['www.pipfix.com']
    env.project_name = 'pipfix'
    env.project_domain = "www.pipfix.com"
    env.nginx_template = 'deploy/conf/nginx.demo.conf'
    env.project_path = '/home/mativs/projects/%s' % env.project_name
