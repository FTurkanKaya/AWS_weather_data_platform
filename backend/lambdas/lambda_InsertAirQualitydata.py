import csv
import psycopg2
import os
import boto3
from datetime import datetime

# S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    inserted_rows = 0

    for record in event.get('Records', []):
        s3_info = record.get('s3')
        if not s3_info:
            print("Skipping record: not an S3 event")
            continue

        bucket_name = s3_info['bucket']['name']
        file_key = s3_info['object']['key']

        print(f"Processing S3 file: s3://{bucket_name}/{file_key}")

        # S3 dosyasını oku
        try:
            obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            data = obj['Body'].read().decode('utf-8').splitlines()
        except s3_client.exceptions.NoSuchKey:
            print(f"⚠ File does not exist: {file_key}")
            continue
        except Exception as e:
            print(f"Error reading S3 file {file_key}: {e}")
            continue

        csv_reader = csv.DictReader(data)

        try:
            # RDS bağlantısı
            conn = psycopg2.connect(
                host=os.environ['RDS_HOST'],
                dbname=os.environ['RDS_DBNAME'],
                user=os.environ['RDS_USER'],
                password=os.environ['RDS_PASSWORD'],
                port=os.environ['RDS_PORT']
            )
            cur = conn.cursor()

            for row in csv_reader:
                city_name = row['city_name'].strip()

                # city_id al
                cur.execute("""
                    SELECT c.cities_id
                    FROM cities c
                    JOIN countries co ON c.country_id = co.countries_id
                    WHERE LOWER(TRIM(c.city_name)) = LOWER(%s)
                """, (city_name,))
                result = cur.fetchone()
                if not result:
                    print(f"City not found: {city_name}")
                    continue
                city_id = result[0]

                # Tarih bilgisi CSV path'ten
                parts = file_key.split('/')
                try:
                    year, month, day = map(int, parts[1:4])
                    data_date = datetime(year, month, day).date()
                except Exception as e:
                    print(f"Error parsing date from file_key: {file_key}, {e}")
                    continue

                # Aynı city_id ve data_date var mı kontrol et
                cur.execute("SELECT 1 FROM air_quality WHERE city_id=%s AND data_date=%s", (city_id, data_date))
                if cur.fetchone():
                    print(f"✔ Data already exists for {city_name} on {data_date}, skipping.")
                    continue

                # Insert işlemi
                cur.execute("""
                    INSERT INTO air_quality (
                        city_id, data_date, air_quality_index, co, no, no2, o3, so2, pm2_5, pm10, nh3
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    city_id, data_date, row['air_quality_index'], row['co'], row['no'],
                    row['no2'], row['o3'], row['so2'], row['pm2_5'], row['pm10'], row['nh3']
                ))
                inserted_rows += 1
                print(f"Inserted row for {city_name} on {data_date}")

            conn.commit()
            cur.close()
            conn.close()

            print(f"✅ Total inserted rows from {file_key}: {inserted_rows}")

        except Exception as e:
            print(f"DB error: {e}")
            continue

    return {"status": "succeeded", "inserted_rows": inserted_rows}
