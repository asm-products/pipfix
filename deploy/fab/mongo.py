from cuisine import package_ensure, package_update
from cuisine import mode_sudo, run

MONGO_REPO = "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen"

def mongodb_ensure():
    with mode_sudo():
        if not run("cat /etc/apt/sources.list | grep '%s'" % (MONGO_REPO
          ), warn_only=True).succeeded:
            run("apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10")
            run("add-apt-repository '%s'" % (MONGO_REPO))
            package_update()
        package_ensure("mongodb-org")