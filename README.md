![alt text](https://github.com/Pivotal-Data-Engineering/gemfire-azure/blob/master/icon_gemfire1.png "Logo")
## Pivotal Gemfire On Microsoft Azure.

##### The repo provide automation for installing Pivotal Gemfire data fabric on Microsoft Azure cloud. Currently support gemfire 9.1.0 and 8.2.6 versions

## Setup
Install the [Azure CLI version 2.0](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest).  
Ensure that the `az` command is on the path.

Locate the public portion of the ssh key you wish to use.  You will need to
provide a the name of a file containing the public key.  You can, for example,
provide ~/.shh/id_rsa.pub or you can create a new key using `ssh-keygen`.  
The contents of the file you provide will be uploaded to the
~/.ssh/authorized_keys file on each deployed server.

Make sure you have authenticated with the CLI: `az login`

## Usage:
clone the repo and run ./gf_deploy.sh

## Current State:
The script read the configuration data from the parameters json file and provision the infrastructure and install jdk, pip, and gemfire software.

## In flight:
1. Integrate with Azure UI
2. Gemfire management scripting.


  Pivotal Gemfire is a licenced Trademark © 2017 Pivotal Software, Inc. All Rights Reserved.
  Microsoft Azure is a licenced trademark of © 2017 Microsoft corporation. All Rights Reserved.
