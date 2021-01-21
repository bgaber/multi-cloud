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

Completion Date
---------------
I expect to have this project finished by 28 February 2021