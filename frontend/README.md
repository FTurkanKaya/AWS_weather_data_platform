# Frontend — AWS Weather Data Platform

Dit is de React frontend voor het Weather Data Platform. De applicatie maakt gebruik van AWS Amplify en Cognito User Pools voor authentisatie.

##  Structuur

```
frontend/
│
├─ public/
├─ src/
│  ├─ config/awsConfig.js
│  ├─ App.js
│  ├─ index.js
│  ├─ aws-exports.js (optioneel)
│  └─ componenten/
├─ package.json
└─ README.md
```

---

##  AWS Cognito Configuratie

De parameters worden geladen vanuit:

- `src/config/awsConfig.js`  
- optioneel: `.env` variabelen zoals:

```
REACT_APP_AWS_REGION=eu-north-1
REACT_APP_COGNITO_DOMAIN=...
REACT_APP_USER_POOL_ID=...
REACT_APP_USER_POOL_CLIENT_ID=...
```

**Let op:** Geen gevoelige data committen.

---

##  Development starten

```bash
npm install
npm start
```

De applicatie draait op:

```
http://localhost:3000
```

---

##  Productie Build

Gebruik één van de opties:

### 1. Build voor S3 / CloudFront
```bash
npm run build
```
Output komt in `/build`.

### 2. Build via Docker (nginx)
```bash
docker build -f ../docker/Dockerfile.frontend -t weather-app .
docker run -p 80:80 weather-app
```

---

##  Functionaliteiten

- Inloggen via Cognito (OAuth2 Authorization Code Flow)
- Dashboard met weerinformatie
- Beheer van favoriete steden
- API-requests naar backend Lambdas
- Grafieken (optioneel via chartbibliotheken)

---

##  Extra

Als je AWS Amplify CLI gebruikt, wordt `aws-exports.js` automatisch aangemaakt.  
Dit bestand **mag in Git** omdat het geen secrets bevat.
