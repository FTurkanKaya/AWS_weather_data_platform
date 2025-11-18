# Backend — AWS Weather Data Platform

De backend bestaat uit serverless AWS Lambda functies geschreven in Python. De functies zijn gekoppeld aan S3, RDS, SES en EventBridge.

## 📁 Structuur

```
backend/
│
├─ lambdas/
│  ├─ get_weather_data.py
│  ├─ update_user_pref.py
│  ├─ send_email_notifications.py
│  ├─ requirements.txt
│
├─ infra/ (optioneel)
│  ├─ template.yaml (AWS SAM)
│  └─ iam_policies.json
│
└─ README.md
```

---

##  Lambda Functies

### `get_weather_data.py`
- Haalt elke 24 uur weergegevens op via externe API.
- Slaat resultaten op in S3 (per dag / maand / jaar).
- Geactiveerd via EventBridge cron.

### `update_user_pref.py`
- CRUD voor gebruikersvoorkeuren (bijv. favoriete steden).
- Verbindt met RDS PostgreSQL.

### `send_email_notifications.py`
- Verstuurt waarschuwingen of updates via SES.
- Gebruikt templated emails (optioneel).

---

## 🗄 Databaseschema (voorbeeld)

```sql
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    UNIQUE(user_id, city)
);
```

---

##  Lokale installatie

```bash
pip install -r lambdas/requirements.txt
```

---

##  Deployment (voorbeeld)

### Direct Lambda upload (ZIP)
```bash
cd ../../scripts
./deploy_lambda.sh get_weather_data
```

### Via AWS SAM
```bash
sam build
sam deploy --guided
```

---

##  Omgevingsvariabelen

Alle Lambda’s gebruiken:

```
AWS_REGION=eu-north-1
WEATHER_API_KEY=
S3_BUCKET=
DB_HOST=
DB_USER=
DB_PASS=
DB_NAME=
SES_FROM_EMAIL=
```

Bewaar deze in:
- AWS Systems Manager Parameter Store  
- AWS Secrets Manager  
- NOOIT in Git

---

##  Testing

- Unit tests met `pytest`
- Handmatige tests via Test Events in lambda console

---

##  Notities

- Voor `psycopg2` is een Lambda Layer of container image aanbevolen.
- S3-paden gebruiken formaat:
  ```
  weather-data/YYYY/MM/DD/city.json
  ```

