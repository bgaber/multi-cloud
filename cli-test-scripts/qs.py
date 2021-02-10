#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def run_quickstart():
    # [START vision_quickstart]
    import io
    import os
    import json

    # Imports the Google Cloud client library
    # [START vision_python_migration_import]
    from google.cloud import vision
    # [END vision_python_migration_import]

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "multi-cloud-vision-api-15ab1c23c633.json"

    # Instantiates a client
    # [START vision_python_migration_client]
    client = vision.ImageAnnotatorClient()
    # [END vision_python_migration_client]

    # The name of the image file to annotate
    file_name = os.path.abspath('resources/wakeupcat.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print(labels)

    print('Labels and Scores:')
    scores = []
    for label in labels:
        print(label.description + " - " + str(label.score))
        scores.append({"description": label.description, "score": label.score})
            
    # Create JSON to be written into Cosmos DB
    print(scores)
    bucketname = "bg-ca-central-1-uploads"
    filename = "wakeupcat.jpg"
    db_dict = {"bucket": bucketname, "filename": filename, "scores": scores}
    print(json.dumps(db_dict, indent = 4))
    # [END vision_quickstart]


if __name__ == '__main__':
    run_quickstart()
