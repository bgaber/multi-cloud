from chalice import Chalice
import boto3
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import json
import os

app = Chalice(app_name='get_cosmosdb_record')

HOST = os.environ['COSMOS_DB_HOST']
MASTER_KEY = os.environ['COSMOS_MASTER_KEY']
DATABASE_ID = os.environ['COSMOS_DATABASE_ID']
CONTAINER_ID = os.environ['COSMOS_CONTAINER_ID']

@app.route('/return_cosmosdb_record', methods=['GET'], cors=True)
def return_cosmosdb_record():
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
            
        # Acquire the Form Get method paramters
        parameters = app.current_request.query_params
        doc_id = parameters['id']
        account_number = parameters['fname']
        response = container.read_item(item=doc_id, partition_key=account_number)
        # send return to CloudWatch Logs
        print(json.dumps(response))
    except exceptions.CosmosHttpResponseError as e:
        print('\nCaught an error. {0}'.format(e.message))

    return json.dumps(response)