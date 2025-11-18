import os
import json
import psycopg2

# RDS bağlantısı
def get_connection():
    return psycopg2.connect(
        host=os.environ['RDS_HOST'],
        database=os.environ['RDS_DB'],
        user=os.environ['RDS_USER'],
        password=os.environ['RDS_PASSWORD']
    )

def lambda_handler(event, context):
    email = event.get('queryStringParameters', {}).get('email')
    if not email:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Email parametresi gerekli"}),
            "headers": {"Access-Control-Allow-Origin": "*"}
        }

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT first_name, last_name, email, country, city 
            FROM users 
            WHERE email = %s
        """, (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Kullanıcı bulunamadı"}),
                "headers": {"Access-Control-Allow-Origin": "*"}
            }

        user = {
            "first_name": row[0],
            "last_name": row[1],
            "email": row[2],
            "country": row[3],
            "city": row[4]
        }

        return {
            "statusCode": 200,
            "body": json.dumps({"user": user}),
            "headers": {"Access-Control-Allow-Origin": "*"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)}),
            "headers": {"Access-Control-Allow-Origin": "*"}
        }
