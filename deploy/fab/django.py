from deploy.fab.virtualenv import virtualenv
from deploy.fab.postgresql import postgresql_database_check, postgresql_database_drop, postgresql_ensure
from deploy.fab.crontab import crontab_ensure
from cuisine import file_update, text_template, dir_ensure
from cuisine import cd, run, mode_sudo, sudo, file_exists
from fabric.api import get, put, local, env, lcd
from fabric.contrib.project import rsync_project


import re
import os

def django_ensure(project_path, project_name, template, config, key_env, venv_path='.venv', migration=''):
    django_config_ensure(project_path, template, config, key_env)
    django_disable_debug_mode(project_path, config)
    django_log_ensure(project_path)
    django_database_ensure(project_path, venv_path)
    django_static_ensure(project_path, venv_path)

def django_enable_debug_mode(project_path, config):
    with cd(project_path):
        file_update(config, lambda x: re.sub('DEBUG = \w*', 'DEBUG = True', x) )

def django_disable_debug_mode(project_path, config):
    with cd(project_path):
        file_update(config, lambda x: re.sub('DEBUG = \w*', 'DEBUG = False', x) )

def django_config_ensure(project_path, template, config, key_env):
    with cd(project_path):
        run("cp %s %s" % (template, config))
        file_update(config, lambda x: text_template(x,key_env))

def django_log_ensure(project_path):
    with cd(project_path):
        dir_ensure('logs')

def django_static_ensure(project_path, venv_path='.venv'):
    with virtualenv(project_path, venv_path):
        run("python manage.py collectstatic --noinput")

def django_database_ensure(project_path, venv_path='.venv', migration=''):
    with virtualenv(project_path, venv_path):
        run("python manage.py migrate %s" % migration)

def django_cache_ensure(project_path, project_name, schedule, venv_path='.venv'):
    script = "%s/bin/python %s/manage.py rebuild_index --noinput" % (
        os.path.join(project_path, venv_path),
        project_path)
    cron_name = "%s-cache" % project_name
    crontab_ensure(schedule, script, cron_name, root=True )
    with virtualenv(project_path, venv_path):
        run('python manage.py clear_cache')

def django_search_ensure(project_path, venv_path='.venv'):
    with virtualenv(project_path, venv_path):
        run("python manage.py build_solr_schema > schema.xml")
        sudo("mv schema.xml /etc/solr/conf/")
        sudo("service tomcat6 restart")
        sudo('python manage.py rebuild_index  --noinput')

def django_replace_data(project_path, sqlite_path, local_media_path, 
        remote_media_path, venv_path='.venv'):
    """ Drop and recreate db with remote data and download media files """
    local("rm -f %s" % sqlite_path)
    django_database_local_setup()
    django_database_pull(project_path, venv_path)
    local("python manage.py loaddata /tmp/db.json")
    django_media_pull(project_path, remote_media_path )
    local("mkdir -p %s" % (local_media_path)) 
    local("rm -rf %s/*" % (local_media_path))
    local("tar -xf /tmp/media.tar.gz -C %s" % (local_media_path)) 

def django_database_local_setup():
    local("python manage.py syncdb --all --noinput")
    local("python manage.py migrate --fake")

def django_database_pull(project_path, venv_path='.venv'):
    """ Download database dump to /tmp/db.json """
    with virtualenv(project_path, venv_path):
        run("python manage.py dumpdata --natural -e sessions -e admin -e contenttypes -e auth.Permission > /tmp/db.json")
        get('/tmp/db.json', '/tmp/db.json')

def django_media_pull(project_path, backup_media_path, remote_media_path):
    """ Download media to /tmp/media.tar.gz """
    rsync_project("%s/%s" % (project_path, remote_media_path), 
            backup_media_path, upload=False)
    
def django_backup(project_path, remote_media_path, venv_path='.venv'):
    """ Backup Server Data """
    parent_dir, backup_name = "backups", "last"
    backup_media_path = "%s/media/" % (parent_dir)
    backup_file = "%s/%s.tar.gz" % (parent_dir, backup_name)

    local("mkdir -p %s" % backup_media_path)
    django_database_pull(project_path, venv_path)
    local("mv /tmp/db.json %s/db.json" % parent_dir)
    django_media_pull(project_path, backup_media_path, remote_media_path )
    with lcd(parent_dir):
        local("rm -rf %s.tar.gz" % (backup_name))
        local('find . -type f -print0 | tar -czf %s.tar.gz --null -T -' % (
            backup_name))

def django_create_superuser(project_path, venv_path='.venv'):
    with virtualenv(project_path, venv_path):
        run('python manage.py createsuperuser')

def django_database_push(project_path, db_name, db_username, db_password, config_template_path, config_path):
    """ Recreate and load local database to remote host"""
    local("python manage.py dumpdata > /tmp/db.json")
    with cd(project_path):
        put('/tmp/db.json', '/tmp/db.json')
    if postgresql_database_check(db_name):
        postgresql_database_drop(db_name)
    django_config_ensure(project_path,
        config_template_path,
        config_path)
    postgresql_ensure(db_name, db_username, project_path, db_password )
    django_database_ensure(project_path )    
    with virtualenv(project_path):
        run("python manage.py loaddata /tmp/db.json")

def django_media_push(project_path, local_media_path, remote_media_path):
    with lcd(local_media_path):
        local('tar -czf /tmp/media.tar.gz *')
    put('/tmp/media.tar.gz', '/tmp/media.tar.gz')
    
    with cd(project_path):
        run("mkdir -p %s" % (remote_media_path)) 
        with cd(remote_media_path):
            run("rm -rf *")
            run("tar -xf /tmp/media.tar.gz") 