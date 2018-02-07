from __future__ import print_function
import jinja2
import os
import os.path
import shutil
import pwd
import sys
import subprocess

def validate_env():
    for key in ['GEMFIRE_USER']:
        if key not in os.environ:
            sys.exit('A required environment variable is not present: ' + key)

if __name__ == '__main__':
    """
    This script installs systemd unit to start and stop the
    GemFire cluster when the machine is started and stopped.

    This script expects the following environment variables
    GEMFIRE_USER the user that will run the GemFire processes
    """
    validate_env()

    # capture environment variables
    runAsUser = os.environ['GEMFIRE_USER']

    # set up the jinja2 template environment
    context = dict()
    context['RunAsUser'] = runAsUser

    # render the template
    jinja2Env = jinja2.Environment(loader = jinja2.FileSystemLoader('/home/{0}/gemfire-azure/init_scripts'.format(run_as_user)), trim_blocks = True, lstrip_blocks = True)

    tplate = jinja2Env.get_template('gemfire.service.tpl')
    target = '/etc/systemd/system/gemfire.service'
    with open(target,'w') as f:
        tplate.stream(context).dump(f)

    // install the service
    subprocess.check_call(['systemctl','enable','gemfire.service'])
