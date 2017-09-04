from __future__ import print_function
import os
import subprocess
import sys

def validate_env():
    for key in ['GEMFIRE_USER']:
        if key not in os.environ:
            sys.exit('A required environment variable is not present: ' + key)


if __name__ == '__main__':
    """
    This script expects the following environment variables
    GEMFIRE_USER
    """
    validate_env()

    gemuser = os.environ['GEMFIRE_USER']
    cluster_home = '/home/{0}/gemfire_cluster'
    java_home = '/usr/java/jdk1.8.0_144'
    gemfire = '/usr/local/gemfire'

    rc = subprocess.call(['sudo','-u',gemuser, 'GEMFIRE={0}'.format(gemfire),'JAVA_HOME={0}'.format(java_home), 'python', 'cluster.py','start'], cwd=cluster_home)
    if (rc == 0):
        print('GemFire cluster started')
    else:
        print('GemFire cluster failed to start')

    return rc
