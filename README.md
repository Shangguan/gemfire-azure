
![alt text](https://github.com/Pivotal-Data-Engineering/gemfire-azure/blob/master/icon_gemfire1.png "Logo") 
## Pivotal Gemfire On Microsoft Azure.
      
##### The repo provide automation for installing Pivotal Gemfire data fabric on Microsoft Azure cloud. Currently support gemfire 9.1.0 and 8.2.6 versions

## Current State:
The scrript read the configuration data from the paramters json file and provision the infrastructure and install jdk, pip, and gemfire software. 

## Deploy template using Azure CLI

Example:


> az account list

> az account set "PDE-spaladugu"

> az group create --location eastus --name "GemfireDatafabricRG"

> az group deployment create --resource-group "GemfireDatafabricRG" --name "datafabricTemplate" --template-file "gemfire_template.json" --parameters-file "gf_mainTemplate.parameters.json"

Note: location and resource group names in the file gf_mainTemplate.parameters.json should match to what we used in step 3.



## In flight:
1. Integrate with Azure UI
2. Gemfire management scripting.






  Pivotal Gemfire is a licenced Trademark © 2017 Pivotal Software, Inc. All Rights Reserved.
  Microsoft Azure is a licenced trademark of © 2017 Microsoft corporation. All Rights Reserved.

