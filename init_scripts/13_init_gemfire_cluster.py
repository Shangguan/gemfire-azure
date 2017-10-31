from __future__ import print_function
import jinja2
import json
import os
import os.path
import random
import shutil
import pwd
import sys
import subprocess

def validate_env():
    for key in ['GEMFIRE_USER', 'CLUSTER_NAME','GF_SUPERUSER_PASS']:
        if key not in os.environ:
            sys.exit('A required environment variable is not present: ' + key)

if __name__ == '__main__':
    """
    This script places a cluster definition and the gemfire-manager cluster
    control scripts in /home/$GEMFIRE_USER/gemfire_cluster

    This script expects the following environment variables
    GEMFIRE_USER the user that will run the GemFire processes
    CLUSTER_NAME the name of the cluster
    GF_SUPERUSER_PASS  the password for the GemFire superuser
    """
    validate_env()

    # parameters
    gf_superuser_pass = os.environ['GF_SUPERUSER_PASS']
    clusterName = os.environ['CLUSTER_NAME']
    gemuser = os.environ['GEMFIRE_USER']

    # check to see if we are the 0th host
    hostname = subprocess.check_output(['hostname']).strip()
    if hostname == clusterName + '-server0':
        cluster_home = '/datadisks/disk1/gemfire_cluster'
        java_home = '/usr/java/jdk1.8.0_144'
        gemfire = '/usr/local/gemfire'

        rc = subprocess.call(['sudo','-u',gemuser, 'GEMFIRE={0}'.format(gemfire),'JAVA_HOME={0}'.format(java_home), 'python', 'cluster.py','start'], cwd=cluster_home)
        if (rc == 0):
            print('First locator started')
        else:
            print('First locator failed to start')
            sys.exit(-1)

    else:
        print('nothing to do for init_gemfire_cluster on this server')
        sys.exit(0)

    # now figure out the locator port and run a gfsh import cluster config
    clusterdef_file = os.path.join(cluster_home,'cluster.json')
    with open(clusterdef_file, 'r') as f:
        cdef = json.load(f)

    locator_port = cdef['locator-properties']['port']
    gfsh = os.path.join(gemfire,'bin','gfsh')
    zipfile_name = os.path.join('/home',gemuser,'gemfire-azure','init_scripts','cluster.zip')

    subprocess.call([gfsh,'-e','connect --user=gfadmin --password= {0} --locator=localhost[{1}]'.format(gf_superuser_pass,locator_port), '-e','import cluster-configuration --zip-file-name={0}'.format(zipfile_name)])
    if (rc == 0):
        print('initial cluster configuration imported')
    else:
        sys.exit('cluster configuration import failed')

    # now signal readiness by starting a simple HttpServer
    subprocess.Popen(['python', '-m', 'SimpleHTTPServer', '80'], cwd=os.path.join('/home',gemuser,'gemfire-azure','init_scripts','http'))
