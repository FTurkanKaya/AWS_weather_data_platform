import psycopg2
import os

def lambda_handler(event, context):
    email = event['userName']  # veya event['request']['userAttributes'].get('email')
    first_name = event['request']['userAttributes'].get('name')  # corrected
    last_name = event['request']['userAttributes'].get('family_name')
    
    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            port=5432
        )
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO users (email, first_name, last_name)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO NOTHING;
        """, (email, first_name, last_name))
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ User {email} added to RDS users table.")
    
    except Exception as e:
        print("❌ Error connecting or inserting to RDS:", e)
    
    return event

