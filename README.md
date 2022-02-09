# ado-work-items
An Azure function to update DevOps work items. It uses a specific query for my username, but you can easily update this to match your own username and your own query.

The WIQL query can be extracted on Azure DevOps. Make sure that the query matches right with the restrictions you need.

The changes for the update are also specific since they are field-specific for my team. If you are looking for something similar, you can use this as a base to try your own function.


## Access Policy and Permissions
The function is also using Keyvault with Access Policy. In order for _that to work_ you will need to create a system account policy for the function and then allow that ID to have access to your KeyVault. The Keyvault must have the token from Azure DevOps.

1. Start by creating a _System Assigned_  managed identity in the function app. You can do this with the Azure CLI by replacing the following command with the correct resource group and function name:

```bash
$ az functionapp identity assign -n $functionAppName -g $resourceGroup
```

Otherwise you can do this in the portal for the function app. Go to Settings --> Identity. Then Select _System Assigned_. Select "On" and then save. Take note on the ID that was generated.

2. Go to the Key Vault and select the previously created Key Vault. Then to Settings --> Access Policy. A radio button showing _Vault Access Policy_ should be selected in order for this to work. Then select on _Add Access Policy_, use the _Key & Secret Management_ template and then _Select Principal_. Search for the ID  from the identity assignment _or_ the name of the function, add it, and save it.
