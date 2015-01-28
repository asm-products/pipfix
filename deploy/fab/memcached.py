from cuisine import package_ensure
from cuisine import file_update, file_exists, file_unlink
from cuisine import text_template
from cuisine import mode_sudo, run, cd

def memcached_ensure():
    with mode_sudo():
        package_ensure('memcached') 