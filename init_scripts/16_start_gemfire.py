from __future__ import print_function
import httplib
import os
import socket
import subprocess
import sys
import time

def validate_env():
    for key in ['GEMFIRE_USER','CLUSTER_NAME','STARTING_PRIVATE_IP','PRIVATE_IP_PREFIX']:
        if key not in os.environ:
            sys.exit('A required environment variable is not present: ' + key)

def waitforprimary():
    for _ in range(300):
        conn = httplib.HTTPConnection(primary_ip)
        try:
            conn.request('GET','/ready')
            response = conn.getresponse()
            if int(response.status) >= 200 and int(response.status) < 300 :
                response.read()
                break
        except socket.error:
            pass
        finally:
            conn.close()

        print('waiting for primary locator')
        time.sleep(3)

if __name__ == '__main__':
    """
    This script expects the following environment variables
    GEMFIRE_USER
    CLUSTER_NAME
    STARTING_PRIVATE_IP
    PRIVATE_IP_PREFIX
    """
    validate_env()

    gemuser = os.environ['GEMFIRE_USER']
    clusterName = os.environ['CLUSTER_NAME']
    start_ip = int(os.environ['STARTING_PRIVATE_IP'])
    private_ip_prefix = os.environ['PRIVATE_IP_PREFIX']

    cluster_home = '/datadisks/disk1/gemfire_cluster'
    java_home = '/etc/alternatives/java_sdk'
    gemfire = '/usr/local/gemfire'

    primary_ip = '{0}{1}'.format(private_ip_prefix,start_ip)

    hostname = subprocess.check_output(['hostname']).strip()
    if hostname != clusterName + '-server0':

        waitforprimary()

        rc = subprocess.call(['sudo','-u',gemuser, 'GEMFIRE={0}'.format(gemfire),'JAVA_HOME={0}'.format(java_home), 'python', 'cluster.py','start'], cwd=cluster_home)

        if (rc == 0):
            print('GemFire cluster started')
        else:
            print('GemFire cluster failed to start')

        sys.exit(rc)
