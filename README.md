![alt text](https://github.com/Pivotal-Data-Engineering/gemfire-azure/blob/master/icon_gemfire1.png "Logo")
## Pivotal GemFire On Microsoft Azure.

##### Automated provisioning of Pivotal GemFire clusters on the Microsoft Azure cloud
Currently supports GemFire version 9.1.0 and 8.2.6.

## Overview
The file _gemfire\_template.json_ can be deployed using the Azure portal. A
unique cluster name, the number of data nodes and the public portion of an
ssh key must be provided.  Several other parameters are optional.

This project also provides a command line deployment script, _deploy.py_. See
below for details.

__Note on SSH key:__ If using the Azure portal to deploy this template, provide
the key material for the _adminSSHPublicKey_ parameter. Provide the entire
contents of a ".pub" file generated by ssh-keygen.  For example, you could use _~/.ssh/id\_rsa.pub_.  If you are using the
_deploy.py_ script, provide the file name for the value of the
_--public-ssh-key-file_ parameter.

## Usage Example
First complete _Setup for Script Based Deployment_ (below).

```
python ./deploy.py --create-resource-group MyTestGroup --location eastus2  --public-ssh-key-file ./azuredev.pub   --datanode-count 2 --cluster-name gemdev1
```

## Setup for Script Based Deployment
Install the [Azure CLI version 2.0](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest).  
Ensure that the `az` command is on the path.

Make sure you have authenticated with the CLI: `az login`

## Developer Notes
A 3 node Vagrant development environment has been included for testing the
initialization scripts.  To test, run `vagrant up`.  The VMs will be provisioned
and the bootstrap will run providing a realistic simulation of the Azure
environment.  To re-run the setup scripts without re-provisioning the virtual
machines, run 'vagrant reload --provision'.


_Pivotal Gemfire is a licenced Trademark © 2017 Pivotal Software, Inc. All Rights Reserved._
_Microsoft Azure is a licenced trademark of © 2017 Microsoft corporation. All Rights Reserved._
