import csv
import boto3
import os
from io import StringIO
import uuid
import hashlib

# AWS S3 client
s3 = boto3.client('s3')

# Environment variables
OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']

# Örnek kullanıcı verileri
users = [
    {"email": "alice@example.com", "password": "password123"},
    {"email": "bob@example.com", "password": "securepass"},
]

# Kullanıcı şehirleri (UserCities)
user_cities = {
    "alice@example.com": [
        {"city_name": "Hasselt", "country_code": "BE"},
        {"city_name": "Maastricht", "country_code": "NL"},
    ],
    "bob@example.com": [
        {"city_name": "Genk", "country_code": "BE"}
    ]
}

def lambda_handler(event, context):
    #  Users CSV
    users_csv = StringIO()
    users_writer = csv.writer(users_csv)
    users_writer.writerow(['user_id', 'email', 'hashed_password'])

    email_to_id = {}
    for user in users:
        # Benzersiz user_id oluştur
        user_id = str(uuid.uuid4())
        email_to_id[user['email']] = user_id

        # Şifreyi hash'le (örnek: SHA256)
        hashed_password = hashlib.sha256(user['password'].encode()).hexdigest()

        users_writer.writerow([user_id, user['email'], hashed_password])
    
    users_key = f"users/users_{context.aws_request_id}.csv"
    s3.put_object(Bucket=OUTPUT_BUCKET, Key=users_key, Body=users_csv.getvalue().encode('utf-8'))
    print(f"✅ Users CSV uploaded: s3://{OUTPUT_BUCKET}/{users_key}")

    #  UserCities CSV
    cities_csv = StringIO()
    cities_writer = csv.writer(cities_csv)
    cities_writer.writerow(['user_id', 'city_name', 'country_code'])

    for email, cities in user_cities.items():
        user_id = email_to_id[email]
        for city in cities:
            cities_writer.writerow([user_id, city['city_name'], city['country_code']])
    
    cities_key = f"user_cities/user_cities_{context.aws_request_id}.csv"
    s3.put_object(Bucket=OUTPUT_BUCKET, Key=cities_key, Body=cities_csv.getvalue().encode('utf-8'))
    print(f"✅ UserCities CSV uploaded: s3://{OUTPUT_BUCKET}/{cities_key}")

    return {
        "statusCode": 200,
        "body": {
            "users_csv": f"s3://{OUTPUT_BUCKET}/{users_key}",
            "user_cities_csv": f"s3://{OUTPUT_BUCKET}/{cities_key}"
        }
    }
