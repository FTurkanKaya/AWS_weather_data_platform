import csv
import psycopg2
import os
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # S3 ve DB bilgileri
    bucket_name = os.environ['S3_BUCKET']
    s3 = boto3.client('s3')

    # DB bağlantısı
    conn = psycopg2.connect(
        host=os.environ['RDS_HOST'],
        dbname=os.environ['RDS_DBNAME'],
        user=os.environ['RDS_USER'],
        password=os.environ['RDS_PASSWORD'],
        port=os.environ['RDS_PORT']
    )
    cur = conn.cursor()

    today = datetime.today()
    last_7_days = [(today - timedelta(days=i)).strftime("%Y/%m/%d") for i in range(7)]

    total_inserted = 0

    for prefix in last_7_days:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"weather-data/{prefix}/")
        if "Contents" not in response:
            continue

        for obj in response['Contents']:
            file_key = obj['Key']
            print(f"Processing {file_key}")
            obj_file = s3.get_object(Bucket=bucket_name, Key=file_key)
            data = obj_file['Body'].read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(data)

            for row in csv_reader:
                city_name = row['city_name'].split('/')[0].strip()
                country_name = row['country_code'].strip()

                # city_id bul
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

                # Dosya adından tarih al
                try:
                    parts = file_key.split('/')
                    data_date = datetime(int(parts[1]), int(parts[2]), int(parts[3])).date()
                except Exception:
                    print(f"Error parsing date from file_key: {file_key}")
                    continue

                # Insert
                cur.execute("""
                    INSERT INTO air_quality (
                        city_id, data_date, air_quality_index, co, no, no2, o3, so2, pm2_5, pm10, nh3
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    city_id, data_date, row['air_quality_index'], row['co'], row['no'],
                    row['no2'], row['o3'], row['so2'], row['pm2_5'], row['pm10'], row['nh3']
                ))

                total_inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "succeeded", "total_inserted_rows": total_inserted}
