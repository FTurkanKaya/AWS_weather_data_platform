# AWS Weather Data Platform

Dit project is een volledige end-to-end oplossing voor het verzamelen, opslaan en visualiseren van weer- en luchtkwaliteitsgegevens. De architectuur maakt gebruik van AWS-diensten zoals Lambda, S3, RDS, EventBridge, Cognito, SES en CloudFront.

##  Projectstructuur

```
AWS_weather_data_platform/
│
├─ backend/            # AWS Lambda functies + infrastructuur
├─ frontend/           # React webapp + authenticatie via Cognito
├─ docker/             # Dockerfile + nginx configuratie voor productie
├─ config/             # .env voorbeelden (GEEN echte secrets)
├─ scripts/            # Automatische deployment scripts
├─ LICENSE
└─ README.md
```

---

##  Functionaliteit

### Backend
- Automatisch ophalen van dagelijkse weerdata via externe API’s.
- Opslaan van ruwe data in Amazon S3 (gestructureerde paden per datum).
- Gebruik van RDS PostgreSQL voor gebruikersvoorkeuren.
- Automatische e-mailnotificaties via AWS SES.
- EventBridge cron jobs voor geplande taken.

### Frontend
- React-applicatie met AWS Cognito authenticatie (Hosted UI + OAuth2).
- Mogelijkheid om steden te volgen en persoonlijke voorkeuren in te stellen.
- Visualisatie van historische gegevens (via S3-objecten of API’s).
- Responsief ontwerp, klaar voor productie.

---

##  Veiligheid

- **Geen secrets in de repository**.  
  Gebruik `.env` + AWS Systems Manager Parameter Store of Secrets Manager.
- IAM-rollen beperken toegang tot alleen noodzakelijke acties.
- Cognito User Pool voor veilige login + OAuth2 flow.

---

##  Installatie

### Vereisten
- Node.js 18+
- Python 3.10+
- AWS CLI (geconfigureerd)
- Docker (voor productiebuild)

### Frontend lokaal starten
```bash
cd frontend
npm install
npm start
```

### Backend Lambda lokaal deployen (voorbeeld)
```bash
cd scripts
./deploy_lambda.sh get_weather_data
```

---

##  Deployment (Productie)

1. **Frontend**
   - Build React → Docker image → push naar ECR → ECS of EC2 → of S3 + CloudFront.
2. **Backend**
   - Deploy Lambda’s via AWS SAM / CDK / CloudFormation of deploy-script.
3. **Database**
   - RDS PostgreSQL configureren + security groepen instellen.
4. **Automatische taken**
   - EventBridge cron voor dagelijkse datacollectie.
5. **Notificaties**
   - SES e-mailtemplate instellen + verified domain.

---

## 🧪 Testing

- Unit tests voor React via Jest & React Testing Library
- Python unittests voor Lambda-services
- Handmatige API-testen via Postman of AWS Console

---

## 📄 Licentie

Dit project valt onder de MIT-licentie.
