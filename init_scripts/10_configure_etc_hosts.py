from __future__ import print_function
import os
import sys

def validate_env():
    for key in ['LOCATOR_COUNT','DATANODE_COUNT','REGION_NAME', 'AZ_SUBSCRIPTION', 'CLUSTER_NAME', 'STARTING_PRIVATE_IP','PRIVATE_IP_PREFIX']:
        if key not in os.environ:
            sys.exit('A required environment variable is not present: ' + key)

def public_name(clustername, subscription, region, index):
    return '{0}-{1}.{2}.cloudapp.azure.com'.format(hostname(clustername, index),subscription, region).lower()

def hostname(clustername, index):
    return '{0}-server{1}'.format(clustername, index)

if __name__ == '__main__':
    """
    This script expects the following environment variables
    LOCATOR_COUNT the number of locators in this cluster
    DATANODE_COUNT the  number of data nodes in this cluster
    REGION_NAME the Azure region where this cluster is deployed
    CLUSTER_NAME the name of the cluster
    AZ_SUBSCRIPTION the name of the user owning this account
    STARTING_PRIVATE_IP
    PRIVATE_IP_PREFIX
    """
    validate_env()

    # parameters
    locators = int(os.environ['LOCATOR_COUNT'])
    dataNodes = int(os.environ['DATANODE_COUNT'])
    region = os.environ['REGION_NAME']
    az_subscription = os.environ['AZ_SUBSCRIPTION']
    clusterName = os.environ['CLUSTER_NAME']
    start_ip = int(os.environ['STARTING_PRIVATE_IP'])
    private_ip_prefix = os.environ['PRIVATE_IP_PREFIX']

    with open('/etc/hosts', 'w') as hostsfile:
        hostsfile.write('127.0.0.1   localhost\n')
        for i in range(locators + dataNodes):
            hostsfile.write('{0}{1}   {2}\n'.format(private_ip_prefix,start_ip + i,public_name(clusterName,az_subscription,region,i)))

    print('rewrote hosts file')
