import json
import os
import psycopg2
import csv
from io import StringIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3

# --- Config ---
RDS_HOST = os.environ['RDS_HOST']
RDS_PORT = int(os.environ.get('RDS_PORT', 5432))
RDS_DB = os.environ['RDS_DB']
RDS_USER = os.environ['RDS_USER']
RDS_PASSWORD = os.environ['RDS_PASSWORD']

S3_BUCKET = os.environ['S3_BUCKET']

GMAIL_USER = os.environ['GMAIL_USER']               # Gmail adresi
GMAIL_APP_PASSWORD = os.environ['GMAIL_APP_PASSWORD']  # Gmail app password

s3 = boto3.client("s3")

# --- Helper Functions ---
def get_connection():
    return psycopg2.connect(
        host=RDS_HOST, port=RDS_PORT, dbname=RDS_DB,
        user=RDS_USER, password=RDS_PASSWORD
    )

def calculate_allergen_level(data):
    try:
        pm2_5 = float(data.get('pm2_5', 0))
        pm10 = float(data.get('pm10', 0))
        o3 = float(data.get('o3', 0))
        no2 = float(data.get('no2', 0))
        so2 = float(data.get('so2', 0))
        co = float(data.get('co', 0))
        nh3 = float(data.get('nh3', 0))
        air_quality_index = float(data.get('air_quality_index', 0))
    except Exception:
        return {"level": "Onbekend", "advice": "Gegevens ontbreken.", "details": []}

    score = (
        pm2_5 / 50 + pm10 / 50 + o3 / 100 + no2 / 100 +
        so2 / 100 + co / 10 + nh3 / 10 + air_quality_index / 5
    )

    details = []
    if pm2_5 > 25: details.append(f"PM2.5 hoog: {pm2_5} µg/m³, kan de luchtwegen irriteren.")
    if pm10 > 50: details.append(f"PM10 hoog: {pm10} µg/m³, veel stof en allergenen.")
    if o3 > 70: details.append(f"Ozon (O3) hoog: {o3} µg/m³, vooral astmapatiënten moeten voorzichtig zijn.")
    if no2 > 40: details.append(f"NO2 hoog: {no2} µg/m³, luchtvervuiling is hoog.")
    if so2 > 20: details.append(f"SO2 hoog: {so2} µg/m³, vervuiling en irriterend.")
    if co > 5: details.append(f"CO hoog: {co} mg/m³, wees voorzichtig in gesloten ruimtes.")
    if nh3 > 1: details.append(f"NH3 hoog: {nh3} µg/m³, geur en allergierisico aanwezig.")
    if air_quality_index > 3: details.append(f"Luchtkwaliteitsindex: {air_quality_index}, algemene vervuiling is verhoogd.")

    if score <= 2:
        return {"level": "Laag", "advice": "De lucht is over het algemeen schoon.", "details": details or ["Luchtkwaliteit is goed, risico's minimaal."]}
    elif score <= 5:
        return {"level": "Gemiddeld", "advice": "Er zijn enkele risico's voor gevoelige personen.", "details": details or ["Lucht is enigszins vervuild, gevoelige groepen moeten opletten."]}
    elif score <= 8:
        return {"level": "Hoog", "advice": "Luchtvervuiling is hoog. Gevoelige personen moeten binnen blijven.", "details": details or ["Veel stof, pollen of vervuilde lucht aanwezig."]}
    else:
        return {"level": "Zeer Hoog", "advice": "Ga niet naar buiten. Alle gevoelige personen moeten voorzichtig zijn.", "details": details or ["Lucht is erg vervuild en vormt een ernstig gezondheidsrisico."]}

def build_email_body(first_name, city_data_list):
    html = f"<html><body><h2>Hallo {first_name},</h2>"
    html += "<p>Hier is de actuele lucht- en polleninformatie voor jouw geselecteerde steden:</p>"

    for city, data in city_data_list.items():
        allergen = calculate_allergen_level(data)
        html += f"<h3>{city}</h3>"
        html += f"<p><strong>Allergieniveau:</strong> {allergen['level']}</p>"
        html += f"<p><strong>Dagelijks advies:</strong> {allergen['advice']}</p>"
        if allergen.get("details"):
            html += "<ul>"
            for d in allergen["details"]:
                html += f"<li>{d}</li>"
            html += "</ul>"
        html += "<hr>"
    html += "<p>Fijne dag en blijf gezond!</p></body></html>"
    return html

def send_email(to_address, subject, html_body):
    msg = MIMEMultipart('alternative')
    msg['From'] = GMAIL_USER
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html'))

    # Gmail SMTP SSL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, to_address, msg.as_string())
        print(f"📧 E-mail verzonden naar {to_address}")

# --- Lambda Handler ---
def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        for record in event['Records']:
            body = json.loads(record['body'])
            s3_record = body['Records'][0]['s3']
            bucket = s3_record['bucket']['name']
            key = s3_record['object']['key']

            # CSV oku
            obj = s3.get_object(Bucket=bucket, Key=key)
            csv_content = obj['Body'].read().decode('utf-8')
            reader = csv.DictReader(StringIO(csv_content))
            weather_data = {row['city_name']: row for row in reader}
            print(f"✅ CSV geladen: {key}")

            # Kullanıcı verilerini RDS’den çek
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.email, u.first_name, up.city
                FROM user_preferences up
                JOIN users u ON up.user_id = u.user_id
                WHERE up.notify_email = TRUE;
            """)
            rows = cursor.fetchall()
            user_data = {}
            for email, first_name, city in rows:
                if email not in user_data:
                    user_data[email] = {"first_name": first_name, "cities": []}
                user_data[email]["cities"].append(city)

            # E-postaları gönder
            for email, info in user_data.items():
                cities = info["cities"]
                first_name = info["first_name"] or email
                city_data_list = {city: weather_data.get(city, {}) for city in cities}
                html_body = build_email_body(first_name, city_data_list)
                send_email(email, "Dagelijks Lucht- en Pollennieuws", html_body)

            cursor.close()
            conn.close()

        return {"statusCode": 200, "body": json.dumps("E-mails verzonden")}

    except Exception as e:
        print("❌ Fout:", e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}