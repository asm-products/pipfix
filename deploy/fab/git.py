from cuisine import package_ensure, dir_exists
from cuisine import cd, run
from fabric.api import env, abort, local, settings, puts

def git_is_origin(path, uri):
    with cd(path):
        return run('git config --get remote.origin.url').endswith(uri)

def git_ensure(repo_path, commit=None):
    '''seed a remote git repository'''
    package_ensure('git')
    if not dir_exists(repo_path):
        run("mkdir -p %s" % (repo_path)) 
    
    if commit is None:
        # if no commit is specified we will push HEAD
        commit = local('git rev-parse HEAD', capture=True)

    # if local('git status --porcelain', capture=True) != '':
    #     abort(
    #         'Working copy is dirty. This check can be overridden by\n'
    #         'importing gitric.api.allow_dirty and adding allow_dirty to your '
    #         'call.')

    with cd(repo_path):
        # initialize the remote repository (idempotent)
        run('git init')

        if run('git rev-parse --verify -q HEAD', warn_only=True) == commit:
            puts('Remote already on commit %s' % commit)
        else:
            # silence git complaints about pushes coming in on the current branch
            # the pushes only seed the immutable object store and do not modify the
            # working copy
            run('git config receive.denyCurrentBranch ignore')

            # a target doesn't need to keep track of which branch it is on so we always
            # push to its "master"
            with settings(warn_only=True):
                push = local(
                    'git push git+ssh://%s@%s:%s%s %s:refs/heads/master' % (
                        env.user, env.host, env.port, repo_path, commit))

            if push.failed:
                abort(
                    '%s is a non-fast-forward\n'
                    'push. The seed will abort so you don\'t lose information. ' % commit)
            
            # checkout a sha1 on a remote git repo
            run('git reset --hard %s' % (commit))