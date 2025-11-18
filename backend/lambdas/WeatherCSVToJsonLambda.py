import boto3
import csv
import io
import json

s3 = boto3.client("s3")
BUCKET_NAME = "city-geo"

def lambda_handler(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        year = (params.get("year") or "").strip()
        month = (params.get("month") or "").strip()
        day = (params.get("day") or "").strip()

        if not all([year, month, day]):
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Eksik tarih parametresi"})
            }

        # 🔹 Fazladan boşluk/newline temizle + sıfır doldur
        month = month.zfill(2)
        day = day.zfill(2)

        prefix = f"weather-data/{year}/{month}/{day}/"
        print("Prefix:", prefix)

        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)

        if "Contents" not in response or len(response["Contents"]) == 0:
            return {
                "statusCode": 404,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "CSV bulunamadı", "prefix": prefix})
            }

        csv_file = next((obj["Key"] for obj in response["Contents"] if obj["Key"].endswith(".csv")), None)

        if not csv_file:
            return {
                "statusCode": 404,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "CSV dosyası bulunamadı", "prefix": prefix})
            }

        obj = s3.get_object(Bucket=BUCKET_NAME, Key=csv_file)
        data = obj["Body"].read().decode("utf-8")

        csv_reader = csv.DictReader(io.StringIO(data))
        result = [{k.strip(): v for k, v in row.items()} for row in csv_reader]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS"
            },
            "body": json.dumps(result)
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Sunucu hatası", "details": str(e)})
        }
