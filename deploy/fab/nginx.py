from cuisine import package_ensure
from cuisine import file_update, file_exists, file_unlink
from cuisine import text_template
from cuisine import mode_sudo, run, cd

def nginx_ensure(project_path, name, template, key_env):
	with mode_sudo(), cd(project_path):
	    package_ensure('nginx') 
	    run("cp %s /etc/nginx/sites-available/%s" % (template, name))
	    file_update('/etc/nginx/sites-available/%s' % name,
            lambda x: text_template(x,key_env))
	    if not file_exists("/etc/nginx/sites-enabled/%s" % name):
	        run("ln -s -t /etc/nginx/sites-enabled /etc/nginx/sites-available/%s " % (
	            name))
	    file_unlink('/etc/nginx/sites-enabled/default')
	    run("service nginx restart")