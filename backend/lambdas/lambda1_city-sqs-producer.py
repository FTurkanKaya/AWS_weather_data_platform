import json
import boto3
import os

# AWS clients
sqs = boto3.client('sqs')
s3 = boto3.client('s3')

# Environment variables
SQS_QUEUE_URL = os.environ['SQS_QUEUE_URL']

def lambda_handler(event, context):
    # S3 trigger eventinden bucket ve key al
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # S3 dosyasını oku
    obj = s3.get_object(Bucket=bucket, Key=key)
    cities = json.loads(obj['Body'].read().decode('utf-8'))
    
    # Her şehri SQS'ye mesaj olarak gönder
    for city in cities:
        sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(city)
        )
        print(f"✅ Sent to SQS: {city['name']}")
    
    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"{len(cities)} cities sent to SQS"})
    }
