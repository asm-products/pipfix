from cuisine import run, sudo

def crontab_ensure(schedule, script, cron_name, root):
    crontab_remove(cron_name, root)
    crontab_add(schedule, script, cron_name, root)

def crontab_remove(cron_name, root=False):
    command = 'crontab -l | sed "/^.*[\']%s[\']/d" | crontab -' % cron_name
    if root:
        sudo(command)
    else:
        run(command)

def crontab_add(schedule, script, cron_name, root=False):
    command = '(crontab -l; echo "%s %s && echo \'%s\'" ) | crontab -' % (
      schedule, script, cron_name)
    if root:
        sudo(command)
    else:
        run(command)
