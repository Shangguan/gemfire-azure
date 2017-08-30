az group create --name gemfire_datafabric_01 --location eastus

az group deployment create --template-file gemfire_template.json --resource-group gemfire_datafabric_01 --parameters gf_mainTemplate.parameters.json
