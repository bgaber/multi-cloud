import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
#import time
import json
import config

# ----------------------------------------------------------------------------------------------------------
# Prerequistes -
#
# 1. An Azure Cosmos account -
#    https://docs.microsoft.com/azure/cosmos-db/create-cosmosdb-resources-portal#create-an-azure-cosmos-db-account
#
# 2. Microsoft Azure Cosmos PyPi package -
#    https://pypi.python.org/pypi/azure-cosmos/
# ----------------------------------------------------------------------------------------------------------

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

def read_items(container):
    print('\nReading All Items\n')

    item_list = list(container.read_all_items(max_item_count=10))
    
    print("Dump of the JSON:")
    print(json.dumps(item_list, indent=3))
    print()

    print('Found {0} items'.format(item_list.__len__()))
    print()
    print('ID : FILENAME : EPOCH')
    for doc in item_list:
        print("{0} : {1} : {2}".format(doc.get('id'), doc.get('image_fname'), doc.get('_ts')))

    print()
    reduced_list = []
    for doc in item_list:
        reduced_list.append({"id": format(doc.get('id')), "image_fname": format(doc.get('image_fname')), "_ts": format(doc.get('_ts'))})
        print('Item Id: {0}'.format(doc.get('id')))
        print('Filename: {0}'.format(doc.get('image_fname')))
        print('Epoch: {0}'.format(doc.get('_ts')))
        print()
        
    #output new reduced json formatted file
    print(json.dumps(reduced_list, indent=3))


def run_reads():
    client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBDotnetQuickstart", user_agent_overwrite=True)
    try:
        # setup database for this sample
        try:
            #db = client.create_database(id=DATABASE_ID)
            db = client.create_database_if_not_exists(id=DATABASE_ID)

        except exceptions.CosmosResourceExistsError:
            #db = client.get_database_client(database=DATABASE_ID)
            pass

        # setup container for this sample
        try:
            container = db.create_container(id=CONTAINER_ID, partition_key=PartitionKey(path='/image_fname'), offer_throughput=400)
            print('Container with id \'{0}\' created'.format(CONTAINER_ID))

        except exceptions.CosmosResourceExistsError:
            container = db.get_container_client(CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(CONTAINER_ID))

        read_items(container)
        
    except exceptions.CosmosHttpResponseError as e:
        print('\nrun_reads has caught an error. {0}'.format(e.message))

    finally:
            print("\nrun_reads done")


if __name__ == '__main__':
    run_reads()
