from deploy.fab.virtualenv import virtualenv
from cuisine import python_package_ensure, package_ensure
from cuisine import text_template
from cuisine import file_update, dir_ensure
from cuisine import sudo, run, mode_sudo, cd
from fabric.api import env


def gunicorn_ensure(project_path, project_name, process_template, 
    process_config, supervisor_template, key_env, venv_path='.venv'):
    gunicorn_process_ensure(
        project_path, process_template, process_config, key_env, venv_path)
    gunicorn_supervisor_ensure(
        project_path, project_name, supervisor_template, key_env)

def gunicorn_process_ensure(path, template, config, key_env, venv_path='.venv'):
    with virtualenv(path, venv_path):
        python_package_ensure('gunicorn')
        run("cp %s %s" % (template, config))
        file_update(config, lambda x: text_template(x,key_env))
        dir_ensure('%s/logs' % path)
        dir_ensure('%s/run' % path)

def gunicorn_supervisor_ensure(project_path, project_name, template, key_env):
    with mode_sudo(), cd(project_path):
        config = '/etc/supervisor/conf.d/%s.conf' % project_name
        package_ensure('supervisor')
        python_package_ensure('setproctitle')
        run("cp %s %s" % (template, config))
        file_update(config, lambda x: text_template(x,key_env))
        run("supervisorctl reread")
        run("supervisorctl update")
        run("supervisorctl restart %s" % (project_name))

def gunicorn_supervisor_restart(project_name):
    with mode_sudo():
        run("supervisorctl restart %s" % project_name)