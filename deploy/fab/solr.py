from deploy.fab.virtualenv import virtualenv
from cuisine import package_ensure
from cuisine import file_update, file_exists, file_link
from cuisine import text_template
from cuisine import dir_ensure, python_package_ensure
from cuisine import mode_sudo, run, cd

def solr_ensure(project_path, venv_path='.venv'):
    with mode_sudo():
        package_ensure('openjdk-7-jdk libxml2-dev libxslt1-dev python-dev') 
        dir_ensure('/usr/java')
        file_link('/usr/lib/jvm/java-7-openjdk-amd64', '/usr/java/default')
        package_ensure('solr-tomcat')
    with virtualenv(project_path, venv_path):
        python_package_ensure('pysolr lxml cssselect')

