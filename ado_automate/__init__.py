import logging

import azure.functions as func

try:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    from azure.devops.v5_1.work_item_tracking.models import JsonPatchOperation
    from azure.devops.v5_1.work_item_tracking.models import Wiql
    from azure.devops.connection import Connection
    from msrest.authentication import BasicAuthentication
except ImportError:
    logging.exception("Missing dependencies, can't complete import")


def get_items(client):
    wiql = Wiql(
        query="""
     SELECT
        [System.Id],
        [System.WorkItemType],
        [System.Title],
        [System.AssignedTo],
        [System.State],
        [System.Tags]
    FROM workitems
    WHERE
        [System.WorkItemType] = 'Content'
        AND [System.State] = 'In Progress'
        AND [System.AssignedTo] = 'Alfredo Deza <alfredodeza@microsoft.com>'
        AND NOT [Custom.TrackingCode] CONTAINS 'academic'
    """
    )
    # restrict result to 10 items
    return client.query_by_wiql(wiql, top=10).work_items


def update_items(items, client):
    for item in items:
        logging.info(f"updating item {item} with id {item.id}")
        client.update_work_item(
            [
                JsonPatchOperation(
                    op="add",
                    path="/fields/Custom.TrackingCode",
                    value=f"/?WT.mc_id=academic-{item.id}-alfredodeza",
                ),
                JsonPatchOperation(
                    op="add", path="/fields/Custom.ApprovedforReuse", value="Yes"
                ),
            ],
            item.id,
        )


def get_token():
    try:
        credential = DefaultAzureCredential()
    except Exception:
        logging.exception("couldn't get credentials initialized")
        raise

    try:
        client = SecretClient(
            vault_url="https://ado-automate.vault.azure.net", credential=credential
        )

        token = client.get_secret("ado-token")
        return token.value
    except Exception:
        logging.exception("Couldn't init the secret client")
        raise


def main(mytimer: func.TimerRequest) -> None:
    token = get_token()
    organization_url = "https://dev.azure.com/devrel"
    credentials = BasicAuthentication("alfredodeza", token)
    connection = Connection(base_url=organization_url, creds=credentials)
    logging.info("created connection object")
    try:
        item_client = connection.clients.get_work_item_tracking_client()
        logging.info("created a work item client")
    except Exception:
        logging.exception("unable to create the work item client")
    items = get_items(item_client)
    update_items(items, item_client)
