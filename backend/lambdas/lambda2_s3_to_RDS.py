import csv
import psycopg2
import os
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # S3 bilgileri
    bucket_name = os.environ['S3_BUCKET']
    file_key = event['file_key']

    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        data = obj['Body'].read().decode('utf-8').splitlines()
    except Exception as e:
        return {"status": "failed", "message": f"Error reading S3 file: {str(e)}"}

    csv_reader = csv.DictReader(data)

    inserted_rows = 0
    try:
        conn = psycopg2.connect(
            host=os.environ['RDS_HOST'],
            dbname=os.environ['RDS_DBNAME'],
            user=os.environ['RDS_USER'],
            password=os.environ['RDS_PASSWORD'],
            port=os.environ['RDS_PORT']
        )
        cur = conn.cursor()

        for row in csv_reader:
            # Şehir adı sadece / öncesi
            city_name = row['city_name'].split('/')[0].strip()
            country_name = row['country_code'].strip()  # CSV’de ülke ismi var

            # Veritabanındaki city_id’yi al
            cur.execute("""
                SELECT c.cities_id
                FROM cities c
                JOIN countries co ON c.country_id = co.countries_id
                WHERE LOWER(TRIM(c.city_name)) = LOWER(%s)
                  AND LOWER(TRIM(co.country_code)) = LOWER(%s)
            """, (city_name, country_name))

            result = cur.fetchone()
            if result is None:
                print(f"City not found: {city_name} / {country_name}")
                continue

            city_id = result[0]

            # Tarih bilgisi CSV yolundan alınabilir
            # Örn: weather-data/2025/10/20/xxx.csv
            try:
                parts = file_key.split('/')
                data_date = datetime(int(parts[1]), int(parts[2]), int(parts[3])).date()
            except Exception as e:
                print(f"Error parsing date from file_key: {file_key}")
                continue

            # Insert query
            cur.execute("""
                INSERT INTO air_quality (
                    city_id, data_date, air_quality_index, co, no, no2, o3, so2, pm2_5, pm10, nh3
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                city_id, data_date, row['air_quality_index'], row['co'], row['no'],
                row['no2'], row['o3'], row['so2'], row['pm2_5'], row['pm10'], row['nh3']
            ))

            inserted_rows += 1

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        return {"status": "failed", "message": f"DB error: {str(e)}"}

    return {"status": "succeeded", "inserted_rows": inserted_rows}
