from __future__ import print_function
import jinja2
import os
import os.path
import random
import shutil
import pwd
import sys

def validate_env():
    for key in ['GEMFIRE_USER','LOCATOR_COUNT','DATANODE_COUNT','REGION_NAME', 'AZ_SUBSCRIPTION', 'CLUSTER_NAME']:
        if key not in os.environ:
            sys.exit('A required environment variable is not present: ' + key)

def gen_clusterdef(cluster_home_dir, run_as_user, uid, gid):
    # set up context
    context = dict()
    context['RunAsUser'] = runAsUser
    context['Servers'] = []

    # these are used with a secure cluster
    # context['GFPeerPassword'] = gf_superuser_pass
    # context['GFAdminPassword'] = gf_superuser_pass

    for n in range(0,locators + dataNodes):
        server = dict()
        server['Hostname'] = clusterName + '-server' + str(n)
        sn = clusterName + '-server' + str(n) + '-' + az_subscription + '.'  + region + '.cloudapp.azure.com'
        server['PublicName'] = sn.lower()
        server['PrivateIP'] = ipPrefix + str(startingIp + n)
        server['XMX'] = xmx
        server['XMN'] = xmn
        server['Roles'] = []

        # assign appropriate roles to each server
        if  n == 0:
            server['Roles'].append('StartJMXManager')

        if n < locators:
            server['Roles'].append('Locator')
        else:
            server['Roles'].append('DataNode')
            if n == locators:
                server['Roles'].append("Rest")

        context['Servers'].append(server)

    # render the template
    jinja2Env = jinja2.Environment(loader = jinja2.FileSystemLoader('/home/{0}/gemfire-azure/init_scripts'.format(run_as_user)), trim_blocks = True, lstrip_blocks = True)

    templates = [('cluster.json.tpl', cluster_home_dir + '/cluster.json')]
    for template, tgt_file in templates:
        tplate = jinja2Env.get_template(template)
        with open(tgt_file,'w') as f:
            tplate.stream(context).dump(f)

        os.chown(tgt_file, uid,gid)

if __name__ == '__main__':
    """
    This script places a cluster definition and the gemfire-manager cluster
    control scripts in /home/$GEMFIRE_USER/gemfire_cluster

    This script expects the following environment variables
    GEMFIRE_USER the user that will run the GemFire processes
    LOCATOR_COUNT the number of locators in this cluster
    DATANODE_COUNT the  number of data nodes in this cluster
    REGION_NAME the Azure region where this cluster is deployed
    CLUSTER_NAME the name of the cluster
    AZ_SUBSCRIPTION the name of the user owning this account
    """
    validate_env()

    #constants
    ipPrefix = '10.0.0.'
    startingIp = 5

    # parameters
    locators = int(os.environ['LOCATOR_COUNT'])
    dataNodes = int(os.environ['DATANODE_COUNT'])
    region = os.environ['REGION_NAME']
    runAsUser = os.environ['GEMFIRE_USER']
    vmSize = 28 * 1024  #for D12sv2
    az_subscription = os.environ['AZ_SUBSCRIPTION']
    clusterName = os.environ['CLUSTER_NAME']

    # used for security
    #gf_superuser_pass = os.environ['GF_SUPERUSER_PASS']

    # calculated parameters
    xmx = 7 * vmSize / 8
    xmn = xmx / 8
    cluster_home_dir = '/datadisks/disk1/gemfire_cluster'

    # obtain runAsUser's information from the password database
    pwdentry = pwd.getpwnam(runAsUser)

    # create the cluster home directory if it does not exist
    if os.path.exists(cluster_home_dir):
        print('cluster home directory ({0}) already exists, continuing'.format(cluster_home_dir))
    else:
        os.makedirs(cluster_home_dir)
        os.chown(cluster_home_dir,pwdentry[2],pwdentry[3])
        print('created cluster home directory: ' + cluster_home_dir)

    # copy cluster control scripts from gemfire-manager to the cluster_home_dir
    for script in ['cluster.py','clusterdef.py','gemprops.py']:
        src = '/home/{0}/gemfire-azure/gemfire-manager/{1}'.format(runAsUser,script)
        tgt = cluster_home_dir + '/' + script
        shutil.copyfile(src, tgt)
        os.chown(tgt,pwdentry[2],pwdentry[3])
    print('copied gemfire-manager control scripts into cluster home directory')

    # generate the cluster defintion file
    gen_clusterdef(cluster_home_dir, runAsUser, pwdentry[2],pwdentry[3])
