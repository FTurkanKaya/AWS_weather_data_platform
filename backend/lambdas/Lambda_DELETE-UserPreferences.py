import json
import os
import psycopg2

# RDS environment değişkenleri
RDS_HOST = os.environ["RDS_HOST"]
RDS_PORT = int(os.environ.get("RDS_PORT", 5432))
RDS_DB = os.environ["RDS_DB"]
RDS_USER = os.environ["RDS_USER"]
RDS_PASSWORD = os.environ["RDS_PASSWORD"]

def lambda_handler(event, context):
    # 🔹 OPTIONS preflight isteğine yanıt
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
            "body": ""
        }

    # 🔹 DELETE isteği
    if event.get("httpMethod") != "DELETE":
        return {
            "statusCode": 405,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Method not allowed"})
        }

    # Query string parametrelerini al
    email = event.get('queryStringParameters', {}).get('email')
    city = event.get('queryStringParameters', {}).get('city')

    if not email or not city:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Email ve city parametreleri gerekli"})
        }

    try:
        # PostgreSQL bağlantısı
        conn = psycopg2.connect(
            host=RDS_HOST,
            port=RDS_PORT,
            dbname=RDS_DB,
            user=RDS_USER,
            password=RDS_PASSWORD,
            connect_timeout=5
        )
        cur = conn.cursor()

        # user_id al
        cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        user_row = cur.fetchone()
        if not user_row:
            cur.close()
            conn.close()
            return {
                "statusCode": 404,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Kullanıcı bulunamadı"})
            }
        user_id = user_row[0]

        # preference sil
        cur.execute(
            "DELETE FROM user_preferences WHERE user_id = %s AND city = %s",
            (user_id, city)
        )
        conn.commit()
        cur.close()
        conn.close()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,Authorization"
            },
            "body": json.dumps({"message": f"{city} başarıyla silindi."})
        }

    except Exception as e:
        print("❌ Hata:", e)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,Authorization"
            },
            "body": json.dumps({"error": str(e)})
        }
