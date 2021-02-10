import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime

import cosmos_config

# ----------------------------------------------------------------------------------------------------------
# Prerequistes -
#
# 1. An Azure Cosmos account -
#    https://docs.microsoft.com/azure/cosmos-db/create-cosmosdb-resources-portal#create-an-azure-cosmos-db-account
#
# 2. Microsoft Azure Cosmos PyPi package -
#    https://pypi.python.org/pypi/azure-cosmos/
# ----------------------------------------------------------------------------------------------------------

HOST = cosmos_config.settings['host']
MASTER_KEY = cosmos_config.settings['master_key']
DATABASE_ID = cosmos_config.settings['database_id']
CONTAINER_ID = cosmos_config.settings['container_id']

def write_item(image_labels_json):
    container = db_connect()

    # Create an Analysis object.
    # This can be saved as JSON as is without converting into rows/columns.
    container.create_item(body=image_labels_json)

def db_connect():
    client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBDotnetQuickstart", user_agent_overwrite=True)
    try:
        # setup database
        try:
            db = client.create_database(id=DATABASE_ID)

        except exceptions.CosmosResourceExistsError:
            pass

        # setup container
        try:
            container = db.create_container(id=CONTAINER_ID, partition_key=PartitionKey(path='/image_fname'), offer_throughput=400)
            print('Container with id \'{0}\' created'.format(CONTAINER_ID))

        except exceptions.CosmosResourceExistsError:
            print('Container with id \'{0}\' was found'.format(CONTAINER_ID))

        return container

    except exceptions.CosmosHttpResponseError as e:
        print('\cosmosdb has caught an error. {0}'.format(e.message))

    finally:
        print("\ncosmosdb done")
