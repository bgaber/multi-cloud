import json
import boto3

expiry=3600

def lambda_handler(event, context):
    # Extract parameters this way because API Gateway encapsulates them (https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html)
    body = json.loads(event['body'])
    bucket = body['bucket']
    key = body['key']

    try:
        presigned_url = boto3.client('s3').generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': bucket,
                'Key': key,
            },
            ExpiresIn=expiry
        )
    except Exception as error:
        return str(error)
    return {
        'statusCode': 200,
        'body': json.dumps(presigned_url)
    }
