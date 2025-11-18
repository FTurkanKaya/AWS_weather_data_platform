import json
import os
import psycopg2

# Environment variables
RDS_HOST = os.environ["RDS_HOST"]
RDS_PORT = int(os.environ.get("RDS_PORT", 5432))
RDS_DB = os.environ["RDS_DB"]
RDS_USER = os.environ["RDS_USER"]
RDS_PASSWORD = os.environ["RDS_PASSWORD"]

def lambda_handler(event, context):
    try:
        # Gelen body'yi parse et
        body_raw = event.get("body", event)
        body = json.loads(body_raw if isinstance(body_raw, str) else json.dumps(body_raw))

        email = body.get("email")
        selected_cities = body.get("selectedCities", [])

        if not email or not selected_cities:
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "email ve selectedCities gerekli"})
            }

        # PostgreSQL bağlantısı
        conn = psycopg2.connect(
            host=RDS_HOST,
            port=RDS_PORT,
            dbname=RDS_DB,
            user=RDS_USER,
            password=RDS_PASSWORD
        )
        cursor = conn.cursor()

        # 1️⃣ Email'den user_id bul
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": f"Kullanıcı bulunamadı: {email}"})
            }
        user_id = result[0]

        # 2️⃣ Mevcut şehirleri al
        cursor.execute("SELECT city FROM user_preferences WHERE user_id = %s", (user_id,))
        existing_cities = {r[0] for r in cursor.fetchall()}

        # 3️⃣ Yeni şehirleri ekle
        for city in selected_cities:
            # city zaten varsa silip tekrar ekle
            if city in existing_cities:
                cursor.execute(
                    "DELETE FROM user_preferences WHERE user_id=%s AND city=%s",
                    (user_id, city)
                )

            # city’den country_id çek
            cursor.execute("SELECT country_id FROM cities WHERE city_name = %s", (city,))
            country_result = cursor.fetchone()
            if not country_result:
                continue  # Eğer şehir bulunamazsa atla veya loglayabilirsiniz
            country_id = country_result[0]

            # user_preferences tablosuna ekle
            cursor.execute(
                """
                INSERT INTO user_preferences (user_id, city, country_id, notify_email)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, city, country_id, True)
            )

        conn.commit()
        cursor.close()
        conn.close()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,Authorization"
            },
            "body": json.dumps({"message": "Şehir tercihleri başarıyla güncellendi."})
        }

    except Exception as e:
        print("Hata:", e)
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
