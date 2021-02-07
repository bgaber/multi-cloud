import boto3
import io
import os
import json
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "resources/multi-cloud-vision-api-15ab1c23c633.json"

def lambda_handler(event, context):
    """Read file from s3 on trigger."""
    s3 = boto3.client("s3")
    if event:
        print("Event: ", event)
        file_obj = event["Records"][0]
        bucketname = str(file_obj['s3']['bucket']['name'])
        print("Bucket Name: ", bucketname)
        filename = str(file_obj['s3']['object']['key'])
        print("File Name: ", filename)

        # Instantiates a client
        # [START vision_python_migration_client]
        client = vision.ImageAnnotatorClient()
        # [END vision_python_migration_client]

        # The name of the image file to annotate
        file_name = os.path.abspath("resources/022.jpg")

        # Loads the image into memory
        fileObj = s3.get_object(Bucket=bucketname, Key=filename)
        file_content = fileObj["Body"].read()

        #with io.open(file_name, 'rb') as image_file:
        #    content = image_file.read()

        image = vision.Image(content=file_content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        # Result of GCP Vision Image Analysis
        print(labels)
        print('Labels and Scores:')
        for label in labels:
            print(label.description + " - " + str(label.score))
    return {
        'statusCode': 200,
        'body': json.dumps('Successful image analysis')
    }
