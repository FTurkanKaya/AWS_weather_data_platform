
import json
import boto3
import os
import csv
import requests
from io import StringIO
from datetime import datetime

# AWS clients
s3 = boto3.client('s3')

# Environment variables
CITY_BUCKET = os.environ['CITY_BUCKET']        # Örn: "city-geo"
CITY_KEY = os.environ.get('CITY_KEY', 'city_names.csv')
OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']    # Örn: "weather-data"
OPENWEATHER_API_KEY = os.environ['OPENWEATHER_API_KEY']

def lambda_handler(event, context):
    try:
        # S3'ten city_names.csv'yi oku
        csv_obj = s3.get_object(Bucket=CITY_BUCKET, Key=CITY_KEY)
        csv_content = csv_obj['Body'].read().decode('utf-8')
        reader = csv.DictReader(StringIO(csv_content))

        # CSV hazırlığı
        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)
        csv_writer.writerow([
            'city_name', 'country_code', 'latitude', 'longitude',
            'air_quality_index', 'co', 'no', 'no2', 'o3', 'so2',
            'pm2_5', 'pm10', 'nh3'
        ])

        for row in reader:
            name = row['name']
            country = row['country']

            # 1️⃣ Koordinatları al
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={name},{country}&limit=1&appid={OPENWEATHER_API_KEY}"
            geo_res = requests.get(geo_url).json()
            if not geo_res:
                print(f"❌ No geo data for {name}")
                continue
            lat = geo_res[0]['lat']
            lon = geo_res[0]['lon']

            # 2️⃣ Hava kirliliği verisini al
            weather_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
            weather_res = requests.get(weather_url).json()
            if 'list' not in weather_res:
                print(f"❌ No weather data for {name}")
                continue
            air = weather_res['list'][0]
            components = air['components']
            aqi = air['main']['aqi']

            # CSV satırını yaz
            csv_writer.writerow([
                name, country, lat, lon, aqi,
                components.get('co'), components.get('no'), components.get('no2'),
                components.get('o3'), components.get('so2'), components.get('pm2_5'),
                components.get('pm10'), components.get('nh3')
            ])
            print(f"✅ Added: {name}")

        # S3 key: weather-data/YYYY/MM/DD/weather_<timestamp>.csv
        today = datetime.utcnow()
        csv_key = f"weather-data/{today.year}/{today.month:02d}/{today.day:02d}/weather_{context.aws_request_id}.csv"

        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=csv_key,
            Body=csv_output.getvalue().encode('utf-8'),
            ContentType='text/csv; charset=utf-8'
        )

        print(f"✅ CSV uploaded: s3://{OUTPUT_BUCKET}/{csv_key}")

        return {"statusCode": 200, "body": f"CSV uploaded: {csv_key}"}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
