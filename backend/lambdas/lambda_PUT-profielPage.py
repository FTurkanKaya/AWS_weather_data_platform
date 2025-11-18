import os
import json
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=os.environ['RDS_HOST'],
        database=os.environ['RDS_DB'],
        user=os.environ['RDS_USER'],
        password=os.environ['RDS_PASSWORD'],
        port=int(os.environ.get('RDS_PORT', 5432))
    )

def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,PUT"
    }

    # Preflight (OPTIONS) isteğini handle et
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": headers}

    try:
        body = json.loads(event.get('body') or "{}")
        email = body.get('email')
        if not email:
            return {"statusCode": 400, "body": json.dumps({"message": "Email gerekli"}), "headers": headers}

        # Güncellenecek alanlar
        fields = {k: v for k, v in body.items() if k != "email"}
        if not fields:
            return {"statusCode": 400, "body": json.dumps({"message": "Güncellenecek alan yok"}), "headers": headers}

        # Dinamik UPDATE
        set_clause = ", ".join(f"{k} = %s" for k in fields.keys())
        values = list(fields.values()) + [email]

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"UPDATE users SET {set_clause}, updated_at = NOW() WHERE email = %s", values)
            conn.commit()
        finally:
            conn.close()

        return {"statusCode": 200, "body": json.dumps({"message": "Profil güncellendi"}), "headers": headers}

    except Exception as e:
        print("Hata:", str(e))
        return {"statusCode": 500, "body": json.dumps({"message": str(e)}), "headers": headers}
