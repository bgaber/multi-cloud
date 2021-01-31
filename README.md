# Multi-Cloud
![Alt text](images/MultiCloud.png?raw=true "Multi-Cloud Architecture")

Goal
----
My goal for this project is to architect and build an image upload and recognition process using no less than three different cloud providers.  At the time of writing I have chosen AWS and Azure as two of the three providers.  The final provider will be either GCP, IBM Cloud, Alibaba or Oracle Cloud.

Expected Outcome
----------------
The outcome I hope to achieve from this project is to gain practical hands-on experience with cloud providers with whom I don't not normally work.

Main Steps
----------
This project will be completed in two phases.  In Phase I the entire solution will be implemented on AWS.  In Phase II the Phase I solution will be broken into three pieces and implemented on three different cloud providers.  Here are the four main steps of Phase II:

1. Create a simple web page that takes a picture via a mobile device or computer webcam.
2. Save that picture to a storage service on **Cloud Provider 1**.
3. Upon saving that image, trigger a serverless process that calls out to an Image Recognition service on 
**Cloud Provider 2**.
4. Take the metadata that was received back from the Image Recognition service and store it, along with a URL path to the original image into a NoSQL database on **Cloud Provider 3**.

Progress To Date
----------------
I have decided to use with AWS, Azure and GCP.
AWS will be Cloud PRovider 1 and I have not decided what I will use Azure and GCP for.  I may use Azure or GCP for the Image Recognition service and I may use Azure or GCP for the NoSQL database.

This is what has been implemented on AWS to date:
* Two S3 buckets:
  * serverless website hosting contents bucket
    * configured as Public
    * configured for Static website hosting
  * upload bucket to receive the picture uploads
    * CORS configuration
    * configure to trigger the second Lambda function
* HTML, jQuery and CSS that receives the S3 Pre-Signed URL and uploads the picture object to the S3 upload bucket
* One of two Lambda functions:
  * the first Lambda function generates the S3 Pre-Signed URLs to PUT the image object
    * deployed using Chalice to automatically create API REST API trigger and IAM role
      * IAM Policy json file for S3 Get Object, Put Object and Put Object ACL
      * Environment variables for S3 upload bucket name and region name in the config.json file

It was necesary to register a DNS domain name with Route 53 and use the CloudFront CDN in order to use the navigator.mediaDevices Mozilla Web API which provides access to connected media input devices like cameras and microphones, as well as screen sharing.

| Cloud Services Used | Reasons |
| :------------------ | :-----: |
| AWS API Gateway | Trigger REST API Lambda function that returns the S3 Pre-Signed URL |
| :------------------ | :-----: |
| AWS Certificate Management Service | SSL for navigator.mediaDevices Mozilla Web API |
| :------------------ | :-----: |
| AWS CloudFront Service | SSL to S3 Static webpage for navigator.mediaDevices Mozilla Web API | 
| :------------------ | :-----: |
| AWS Lambda | S3 Presigned URL Generation and interact with Azure and GCP for image analysis |
| :------------------ | :-----: |
| AWS Route 53 | Create domain that can be used with CloudFront to route SSL (HTTPS) traffic to HTTP S3 Static website |
| :------------------ | :-----: |
| AWS S3 | Buckets for hosting static web content and receiving image uploads |
| :------------------ | :-----: |
| Azure | CosmosDB or ...
| :------------------ | :-----: |
| GCP | ... |
| :------------------ | :-----: |

Remaining Work To Be Completed
------------------------------
* Write the second Lambda function that will be triggered by S3 whenever a picture is uploaded and then communicates with Azure and GCP to perform the Image Recognition and NoSQL tasks.
* Configure the Image Recognition Service
* Configure the NoSQL database
* Create HTML and Javascript to display the final results

Expected Completion Date
------------------------
I expect to have this project finished by 14 February 2021
