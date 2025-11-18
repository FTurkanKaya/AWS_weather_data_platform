import boto3
import csv
import io
import json
from urllib.parse import unquote_plus

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Tarih parametrelerini query string'den al
        params = event.get("queryStringParameters") or {}
        year = params.get("year")
        month = params.get("month")
        day = params.get("day")

        if not all([year, month, day]):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Eksik tarih parametresi"})
            }

        bucket_name = "city-geo"
        prefix = f"weather-data/{year}/{month}/{day}/"

        # 1️⃣ S3 klasöründeki dosyaları listele
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if "Contents" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "CSV bulunamadı"})
            }

        # 2️⃣ En güncel dosyayı seç
        latest_file = max(response["Contents"], key=lambda x: x["LastModified"])["Key"]

        # 3️⃣ Dosyayı al
        obj = s3.get_object(Bucket=bucket_name, Key=latest_file)
        data = obj["Body"].read().decode("utf-8")

        # 4️⃣ CSV'i JSON'a çevir
        csv_reader = csv.DictReader(io.StringIO(data))
        result = [row for row in csv_reader]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Sunucu hatası", "details": str(e)})
        }
