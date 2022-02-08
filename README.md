# ado-work-items
An Azure function to update DevOps work items. It uses a specific query for my username, but you can easily update this to match your own username and your own query.

The WIQL query can be extracted on Azure DevOps. Make sure that the query matches right with the restrictions you need. 

The changes for the update are also specific since they are field-specific for my team. If you are looking for something similar, you can use this as a base to try your own function.

The function is also using Keyvault with Access Policy. In order for _that to work_ you will need to create a system account policy for the function and then allow that ID to have access to your KeyVault. The Keyvault must have the token from Azure DevOps.
