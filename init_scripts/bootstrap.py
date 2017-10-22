from __future__ import print_function
import argparse
import os
import pwd
import shutil
import subprocess
import sys
import time

TIME_FORMAT = '%Y-%m-%s %H:%M%S %Z'
GIT_URL = 'https://github.com/Pivotal-Data-Engineering/gemfire-azure.git'

class AbortBootstrap(Exception):
    def __init__(self):
        Exception.__init__(self)

def logmsg(msg):
    return '{0} {1}\n'.format(time.strftime(TIME_FORMAT),msg)


def parse_env_args(listofargs):
    """
    parse arguments are added to this processes environment which means
    they will be inherited by forked processes
    """
    for arg in listofargs:
        i = arg.find('=')
        if i == -1:
            continue

        key = arg[0:i]
        val = arg[i+1:]
        os.environ[key] = val

def validate_env(log):
    if 'GEMFIRE_USER' not in os.environ:
        log.write(logmsg('require parameter ({0}) not present in environment.'))
        raise AbortBootstrap()

def run(cmd, log, wd = None):
    process = subprocess.Popen(cmd.split(), stdout=log,stderr = subprocess.STDOUT, cwd=wd)
    out, err = process.communicate()
    if process.returncode != 0:
        raise AbortBootstrap()

def setup_git(owner, branch, log):
    # first be sure git is installed
    run('yum install -y git',log)

    # if the git repo exists, remove it (note, we could update it instead)
    repo_path = '/home/{0}/gemfire-azure'.format(owner)
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
        log.write(logmsg('removed existing gemfire azure repo at {0}'.format(repo_path)))

    # then run git clone and git checkout
    run('sudo -u {0} git clone {1}'.format(owner,GIT_URL), log, wd = '/home/' + owner)
    run('sudo -u {0} git checkout {1}'.format(owner, branch),log, wd = '/home/{0}/gemfire-azure'.format(owner))
    run('sudo -u {0} git submodule init'.format(owner),log, wd = '/home/{0}/gemfire-azure'.format(owner))
    run('sudo -u {0} git submodule update'.format(owner),log, wd = '/home/{0}/gemfire-azure'.format(owner))


if __name__ == "__main__":
    """
    pass the name of a git branch or tag to pull init scripts from using --git-branch mybranch
    pass all environment parameters with --environment name1=val1 name2=val2 ...

    note that currently, passing values that contain spaces is not supported

    bootstrap expects the following parameters to be present in the environment

    GEMFIRE_USER  the name of the user that will run GemFire
    """
    parser = argparse.ArgumentParser('The GemFire on Azure bootstrap')
    parser.add_argument('--git-branch',required = True)
    parser.add_argument('--environment', required = True, nargs = '*')
    args = parser.parse_args()

    with open('/var/log/cloud-init.log','w') as log:
        try:
            log.write(logmsg('bootstrap started'))
            parse_env_args(args.environment)
            validate_env(log)
            gemuser = os.environ['GEMFIRE_USER']

            setup_git(gemuser,args.git_branch,log)
            scripts = os.listdir('/home/{0}/gemfire-azure/init_scripts'.format(gemuser))
            scripts.sort()
            for script in scripts:
                if script == 'bootstrap.py':
                    continue

                if script.endswith('.py'):
                    interpreter = 'python'
                elif script.endswith('.sh'):
                    interpreter = 'sh'
                else:
                    continue

                log.write(logmsg('running {0}'.format(script)))
                run('{2} /home/{0}/gemfire-azure/init_scripts/{1}'.format(gemuser,script, interpreter), log)

        except Exception as x:
            log.write(logmsg('An unexpected exception interrupted the bootstrap.\n' + str(x)))
            sys.exit(1)
