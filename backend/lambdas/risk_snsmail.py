import json
import boto3
import os

# Environment variable kontrolleri
sqs_queue_url = os.environ.get('SQS_QUEUE_URL')
sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')

if not sqs_queue_url or not sns_topic_arn:
    raise Exception("Environment variable eksik: SQS_QUEUE_URL veya SNS_TOPIC_ARN")

# AWS client'ları
sqs = boto3.client('sqs')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # SQS'den mesajları al
    messages = sqs.receive_message(
        QueueUrl=sqs_queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=5
    )

    if 'Messages' not in messages:
        return {'statusCode': 200, 'body': 'SQS boş'}

    for msg in messages['Messages']:
        body = json.loads(msg['Body'])

        # Burada OpenWeather Air Pollution verisi bekleniyor
        location = body.get('location', 'Bilinmeyen')
        aqi = body.get('aqi', -1)
        pm25 = body.get('components', {}).get('pm2_5', 0)
        pm10 = body.get('components', {}).get('pm10', 0)

        # Basit risk skoru
        if aqi <= 50 and pm25 <= 12 and pm10 <= 20:
            risk = "Düşük"
        elif aqi <= 100 or pm25 <= 35 or pm10 <= 50:
            risk = "Orta"
        else:
            risk = "Yüksek"

        # SNS mesajı oluştur
        message_text = f"{location} bölgesi için hava kalitesi uyarısı: Risk seviyesi {risk} (AQI={aqi}, PM2.5={pm25}, PM10={pm10})"

        # UTF-8 encode ile publish
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=message_text,
            Subject=f"{location} Hava Kalitesi Uyarısı"
        )

        # Mesajı SQS'den sil
        sqs.delete_message(
            QueueUrl=sqs_queue_url,
            ReceiptHandle=msg['ReceiptHandle']
        )

    return {
        'statusCode': 200,
        'body': f"{len(messages['Messages'])} mesaj işlendi ve SNS'e gönderildi."
    }
