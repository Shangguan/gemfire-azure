az group create --name GemfireDatafabricRG --location eastus

az group deployment create --template-file gemfire_template.json --resource-group GemfireDatafabricRG --parameters gf_mainTemplate.parameters.json
