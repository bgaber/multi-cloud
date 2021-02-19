# Multi-Cloud
![Alt text](images/MultiCloud.png?raw=true "Multi-Cloud Architecture")

Goal
----
My goal when I began this project was to design and build an image upload and recognition process using no less than three different cloud providers.  In the end I achieved my goal.

Outcome
-------
In completing this propject I was able to gain practical hands-on experience with cloud providers with whom I don't not normally work.

Main Steps
----------
This project was completed in two phases.  In Phase I the entire solution will be implemented on AWS.  In Phase II the Phase I solution will be broken into three pieces and implemented on three different cloud providers.  Here are the four main steps of Phase II:

1. Create a simple web page that takes a picture via a mobile device or computer webcam.
2. Save that picture to a storage service on **Cloud Provider 1**.
3. Upon saving that image, trigger a serverless process that calls out to an Image Recognition service on 
**Cloud Provider 2**.
4. Take the metadata that was received back from the Image Recognition service and store it, along with a URL path to the original image into a NoSQL database on **Cloud Provider 3**.

Solution
--------
AWS, Azure and GCP were used to complete this project.
AWS is Cloud Provider 1, GCP is Cloud Provider 2 and  Azure is Cloud Provider 3.  AWS was used for the S3 serverless hosting of the website and the Lambda functions.  GCP Vision was used for the Image Recognition service and Azure Cosmos DB was used for the NoSQL database.

![Alt text](images/multi-cloud.png?raw=true "Brian's Multi-Cloud Architecture")

These requirements were implemented on AWS Services:
* Two S3 buckets:
  * serverless website hosting contents bucket
    * configured as Public
    * configured for Static website hosting
  * upload bucket to receive the picture uploads
    * CORS configuration
    * configure to trigger the second Lambda function
* HTML, jQuery and CSS that receives the S3 Pre-Signed URL and uploads the picture object to the S3 upload bucket
* Four Lambda functions, three of which are deployed using AWS Chalice:
  * the first Lambda function generates the S3 Pre-Signed URLs to PUT the image object
    * deployed using Chalice to automatically create an API REST API trigger and associated IAM role
      * IAM Policy json file for S3 Get Object, Put Object and Put Object ACL
      * Environment variables for S3 upload bucket name and region name in the config.json file
  * the second Lambda function that is triggered by S3 whenever a picture is uploaded and then communicates with the GCP Vision to perform the Image Recognition and outputs the GCP Vision image analysis results to 
  CloudWatch Logs and will be sent to Azure CosmosDB NoSQL tasks.
  * the third Lambda function returns the id, image_fname (primary key) and _ts (timestamp) of all items from the container in the Azure Cosmos DB
    * deployed using Chalice to automatically create an API REST API trigger and associated IAM role
      * IAM Policy json file for S3 Get Object, Put Object and Put Object ACL
      * Environment variables for S3 upload bucket name and region name in the config.json file
      * The returned data (id, image_fname and _ts) is displayed using JavaScript in a HTML table
  * the fourth Lambda function returns all data of one item from the Azure Cosmos DB based on the id and primary key
    * deployed using Chalice to automatically create and API REST API trigger and associated IAM role
      * IAM Policy json file for S3 Get Object, Put Object and Put Object ACL
      * Environment variables for S3 upload bucket name and region name in the config.json file
      * The GCP Vision API score portion of returned data is displayed alongside the actual image using Javascript in a HTML table
  
These tasks were implemented on GCP and Azure:
* Configured the GCP Vision Image Recognition Service
* Configured the Azure CosmosDB NoSQL database

It was necesary to register a DNS domain name with Route 53 and use the CloudFront CDN in order to use the navigator.mediaDevices Mozilla Web API which provides access to connected media input devices like cameras and microphones, as well as screen sharing.

| Cloud Services Used | Reasons |
| :-----------------: | :-----: |
| AWS API Gateway | Trigger REST API Lambda function that returns the S3 Pre-Signed URL |
| AWS Certificate Management Service | SSL for navigator.mediaDevices Mozilla Web API |
| AWS CloudFront Service | SSL to S3 Static webpage for navigator.mediaDevices Mozilla Web API | 
| AWS Lambda | S3 Presigned URL Generation and interact with Azure and GCP for image analysis |
| AWS Route 53 | Create domain that can be used with CloudFront to route SSL (HTTPS) traffic to HTTP S3 Static website |
| AWS S3 | Buckets for hosting static web content and receiving image uploads |
| Azure | CosmosDB |
| Chalice | Deploy Lambda with API Gateway Trigger |
| GCP | Vision |

Remaining Work To Be Completed
------------------------------
* Enhance HTML and Javascript to display the image analysis results
