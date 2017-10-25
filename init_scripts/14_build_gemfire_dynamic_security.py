import os
import os.path
import pwd
import shutil
import subprocess


MAVEN = '/usr/local/maven/bin/mvn'

if __name__ == '__main__':
    """
    This script expects the following environment variables:

    GEMFIRE_USER the user that will run the GemFire processes
    """
    # runAsUser = os.environ['GEMFIRE_USER']
    # build_dir = '/home/{0}/gemfire-azure/gemfire-dynamic-security'.format(runAsUser)
    #
    # p = subprocess.Popen(['sudo', '-u', runAsUser, MAVEN, 'package'], cwd = build_dir,  stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    # output = p.communicate()
    # if p.returncode != 0:
    #     raise Exception('maven build failed with the following output: {0}'.format(output[0]))
    #
    # print 'built gemfire-dynamic-security'
    pass
