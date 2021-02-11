import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
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
# Sample - demonstrates the basic CRUD operations on a Item resource for Azure Cosmos
# ----------------------------------------------------------------------------------------------------------

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

def read_item(container, doc_id, account_number):
    print('\n1.2 Reading Item by Id\n')

    # We can do an efficient point read lookup on partition key and id
    response = container.read_item(item=doc_id, partition_key=account_number)
    
    #print("Dump of the JSON:")
    #print(json.dumps(response))
    #print()
    #print('Item read by Id {0}'.format(doc_id))
    #print('Scores: {0}'.format(response.get('scores')))
    
    # Loop through list
    #for x in response.get('scores'):
    #    print(x) 
        
    # Loop through list, then through dictionary
    for thisdict in response.get('scores'):
        print("{0}: {1}".format(thisdict["description"], thisdict["score"]))


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

        rcdId = input("Enter the record id: ")
        fname = input("Enter the filename of the image: ")
        read_item(container, rcdId, fname)
        
    except exceptions.CosmosHttpResponseError as e:
        print('\nrun_reads has caught an error. {0}'.format(e.message))

    finally:
            print("\nrun_reads done")


if __name__ == '__main__':
    run_reads()
