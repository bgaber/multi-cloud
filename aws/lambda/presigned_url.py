import json
import boto3
#from botocore.exceptions import ClientError

#bucket='bg-us-east-1-bucket'
#key='filename.jpg'
expiry=3600

def lambda_handler(event, context):
    """
    Method to get url from s3
    :param bucket: name of s3 bucket
    :param key: key of the file
    :return:
    """
    
    #print("Received event: " + json.dumps(event, indent=2))
    #print("s3_bucket_value = " + event['bucket'])
    #print("s3_key_value = " + event['key'])
    #return event['bucket']  # Echo back the first key value
    #raise Exception('Something went wrong')
    try:
        presigned_url = boto3.client('s3').generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': event['bucket'],
                'Key': event['key'],
            },
            ExpiresIn=expiry
        )
    except Exception as error:
        return str(error)
    return {
        'statusCode': 200,
        'body': json.dumps(presigned_url)
    }
