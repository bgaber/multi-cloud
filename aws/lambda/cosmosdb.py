import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
import os

# ----------------------------------------------------------------------------------------------------------
# Prerequistes -
#
# 1. An Azure Cosmos account -
#    https://docs.microsoft.com/azure/cosmos-db/create-cosmosdb-resources-portal#create-an-azure-cosmos-db-account
#
# 2. Microsoft Azure Cosmos PyPi package -
#    https://pypi.python.org/pypi/azure-cosmos/
# ----------------------------------------------------------------------------------------------------------

HOST = os.environ['COSMOS_DB_HOST']
MASTER_KEY = os.environ['COSMOS_MASTER_KEY']
DATABASE_ID = os.environ['COSMOS_DATABASE_ID']
CONTAINER_ID = os.environ['COSMOS_CONTAINER_ID']

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
            #db = client.create_database(id=DATABASE_ID)
            db = client.create_database_if_not_exists(id=DATABASE_ID)

        except exceptions.CosmosResourceExistsError:
            #db = client.get_database_client(database=DATABASE_ID)
            pass

        # setup container
        try:
            container = db.create_container(id=CONTAINER_ID, partition_key=PartitionKey(path='/image_fname'), offer_throughput=400)
            print('Container with id \'{0}\' created'.format(CONTAINER_ID))

        except exceptions.CosmosResourceExistsError:
            container = db.get_container_client(CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(CONTAINER_ID))

        return container

    except exceptions.CosmosHttpResponseError as e:
        print('\ncosmosdb has caught an error. {0}'.format(e.message))

    finally:
        print("\ncosmosdb done")
