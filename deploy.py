from __future__ import print_function

import argparse
import json
import os.path
import subprocess
import sys

# global variables
azureregions = [
  "australiaeast",
  "australiasoutheast",
  "brazilsouth",
  "canadacentral",
  "canadaeast",
  "centralindia",
  "centralus",
  "eastasia",
  "eastus",
  "eastus2",
  "japaneast",
  "japanwest",
  "koreacentral",
  "koreasouth",
  "northcentralus",
  "northeurope",
  "southcentralus",
  "southeastasia",
  "southindia",
  "uksouth",
  "ukwest",
  "westcentralus",
  "westeurope",
  "westus",
  "westus2"
]

def detect_git_branch():
    """
    returns 'master' in the event of any failure
    """
    process = subprocess.Popen(['git','branch'], stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
    out, err = process.communicate()
    if process.returncode != 0:
        return master

    for line in out.splitlines():
        if '*' in line:
            words = line.split()
            if len(words) == 2:
                return words[1]

    return 'master'

def parseArgs():
    parser = argparse.ArgumentParser(description = 'This script deploys a GemFire cluster on Azure')
    allgroup = parser.add_argument_group('arguments')
    allgroup.add_argument('--cluster-name', required=True, help='A unique name for the cluster.')
    allgroup.add_argument('--use-resource-group', help='The name of an existing resource group in which to deploy the GemFire cluster.')
    allgroup.add_argument('--admin-username', required=True, help='The username for SSH access to the deployed virtual machines')
    allgroup.add_argument('--admin-password', required=False, help='SSH password.  If provided, password login for <admin-username> will be enabled on all machined. Cannot be combined with the --public-ssh-key-file argument.')
    allgroup.add_argument('--public-ssh-key-file',type=argparse.FileType('rb'), required = False, help='The path to a file containing the public half of the ssh key you will use to access the servers. May be .pub or .pem')
    allgroup.add_argument('--create-resource-group', help='The name of a new resource group.  The GemFire cluster will be deployed in this group after it is created. This option is incompatible with --use-resource-group.')
    allgroup.add_argument('--resource-group-location', help='The Azure location where the new resource group will be created.  This option must be supplied if --create-resource-group is supplied.This option is incompatible with --use-resource-group.', choices = azureregions)
    allgroup.add_argument('--resource-location', required=True,  help='The Azure location where the new resources will be created.  This is separate from the location of the resource group.', choices = azureregions)
    allgroup.add_argument('--datanode-count', type=int, required = True, choices=range(2,16), help='Number of data nodes that will be deployed.')

    try:
        args = parser.parse_args()
    except IOError as ioe:
        if ioe.filename is not None:
            sys.exit('{0}: {1}'.format(ioe.strerror, ioe.filename))
        else:
            sys.exit(ioe.strerror)

    if args.use_resource_group is None and args.create_resource_group is None:
        sys.exit('one of  --use-resource-group and  --create_resource_group must be supplied')

    if args.use_resource_group is not None and args.create_resource_group is not None:
        sys.exit('only one of  --use-resource-group and  --create_resource_group can be supplied')

    if args.create_resource_group is not None and args.resource_group_location is None:
        sys.exit('--resource_group_location must be supplied whenever --create-resource-group is given')

    if args.admin_password is not None and args.public_ssh_key_file is not None:
        sys.exit('only one of --public-ssh-key-file and --admin-password can be supplied')


    return args

def azrun_list(cmds):
    """
    runs an Azure cli command and parses the results as json
    this method calls sys.exit if the command is not successful
    """
    print('running ' + ' '.join(cmds))
    proc = subprocess.Popen(['az'] + cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin = subprocess.PIPE , cwd = here)
    out, err = proc.communicate()
    if proc.returncode != 0:
        sys.exit('An error occurred while executing ({0}): {1}'.format('az ' + ' '.join(cmds), err))

    return json.loads(out)

def azrun(cmds):
    """
    runs an Azure cli command and parses the results as json
    this method calls sys.exit if the command is not successful
    """
    return azrun_list(cmds.split())

def resource_group_exists(rgname):
    """
    return True if the resource group exists or False if not
    """
    listgroups = azrun('group list')
    for group in listgroups:
        if group['name'] == rgname:
            return True

    return False

def create_resource_group(name, location):
    azrun('group create --name {0} --location {1}'.format(name, location))

def read_key_file(filehandle):
    """
    If the filehandle.name ends with .pub, ssh-keygen will be invoked to convert it
    to .pem format.  filehandle will be closed.
    """
    filename = filehandle.name
    if filename.endswith('.pub'):
        filehandle.close()
        sshkeygen = subprocess.Popen(['ssh-keygen','-f',filename, '-e','-m','pem'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        out, err = sshkeygen.communicate()
        if sshkeygen.returncode != 0:
            sys.exit('An error occurred while reading the key file ({0}) : {1}'.format(sshkeygen.returncode, out))
        else:
            sshkey = out
    else:
        sshkey = filehandle.read(16384)
        filehandle.close

    return sshkey


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(sys.argv[0]))

    args = parseArgs()

    # create the resource group, or verify an existing one
    resourcegroup = None
    if args.use_resource_group is not None :
        if resource_group_exists(args.use_resource_group):
            resourcegroup= args.use_resource_group
        else:
            sys.exit('The specified resource group ({0}) does not exist.'.format(args.use_resource_group))
    else:
        if resource_group_exists(args.create_resource_group):
            sys.exit('Cannot create the resource group ({0}) because it already exists'.format(args.create_resource_group))

        create_resource_group(args.create_resource_group, args.resource_group_location)
        resourcegroup = args.create_resource_group

    # retrieve the ssh key material
    if args.public_ssh_key_file:
        sshkey = args.public_ssh_key_file.read(17384)
        args.public_ssh_key_file.close()
        authentication_type = 'sshPublicKey'
    else:
        authentication_type = 'password'
        sshkey = ''

    # compose the az command  sshPublicKey
    overrides = ['--parameters', 'clusterName={0}'.format(args.cluster_name)]
    overrides.append('adminUserName={0}'.format(args.admin_username))
    overrides.append('authenticationType={0}'.format(authentication_type))
    overrides.append('adminPassword={0}'.format(args.admin_password))
    overrides.append('sshPublicKey={0}'.format(sshkey))
    overrides.append('gemfireDatanodeCount={0}'.format(args.datanode_count))
    overrides.append('gemfireOnAzureProjectTag={0}'.format(detect_git_branch()))
    overrides.append('location={0}'.format(args.resource_location))


    print('Deployment has begun.  This may take a while. Use the Azure portal to view progress...')
    azrun_list(['group', 'deployment', 'create', '--resource-group', resourcegroup, '--template-file', os.path.join(here, 'mainTemplate.json')] + overrides)
    print('GemFire cluster deployed.')
