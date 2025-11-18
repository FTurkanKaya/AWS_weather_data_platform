import json
import os
import psycopg2

RDS_HOST = os.environ["RDS_HOST"]
RDS_PORT = int(os.environ.get("RDS_PORT", 5432))
RDS_DB = os.environ["RDS_DB"]
RDS_USER = os.environ["RDS_USER"]
RDS_PASSWORD = os.environ["RDS_PASSWORD"]

def lambda_handler(event, context):
    print("Received event:", event)

    # Email parametresi kontrolü
    email = event.get("queryStringParameters", {}).get("email")
    if not email:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "email parametresi eksik"})
        }

    try:
        # PostgreSQL bağlantısı
        conn = psycopg2.connect(
            host=RDS_HOST, port=RDS_PORT, dbname=RDS_DB,
            user=RDS_USER, password=RDS_PASSWORD
        )
        cur = conn.cursor()

        # user_id al
        cur.execute("SELECT user_id FROM users WHERE email=%s", (email,))
        user_row = cur.fetchone()
        if not user_row:
            return {
                "statusCode": 404,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Kullanıcı bulunamadı"})
            }
        user_id = user_row[0]

        # sadece şehirleri getir
        cur.execute("""
            SELECT city
            FROM user_preferences
            WHERE user_id = %s AND notify_email = TRUE
        """, (user_id,))
        rows = cur.fetchall()
        preferences = [{"city": r[0]} for r in rows]

        cur.close()
        conn.close()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"preferences": preferences})
        }

    except Exception as e:
        print("❌ Hata:", e)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
