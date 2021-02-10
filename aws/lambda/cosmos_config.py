import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://gcp-vision-response.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'nwyHV7x5lCoruiE6msyaKJcdzOyCdJaya8T1j9GPct7cNJ5ABGZvpr0aA9u89dIEDawktM56ESL8KKAmwee7BQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'ImageAnalysis'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Analyses'),
}