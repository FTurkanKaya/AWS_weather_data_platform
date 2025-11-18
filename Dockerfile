# ---------- BUILD STAGE ----------
FROM node:18 AS build
WORKDIR /app

# build-time envs (örnek: REACT_APP_API_URL, REACT_APP_COGNITO_POOL_ID)
ARG REACT_APP_API_URL
ARG REACT_APP_COGNITO_POOL_ID
ARG REACT_APP_COGNITO_CLIENT_ID

# make them available to npm run build
ENV REACT_APP_API_URL=${REACT_APP_API_URL}
ENV REACT_APP_COGNITO_POOL_ID=${REACT_APP_COGNITO_POOL_ID}
ENV REACT_APP_COGNITO_CLIENT_ID=${REACT_APP_COGNITO_CLIENT_ID}

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# ---------- PRODUCTION STAGE ----------
FROM nginx:stable-alpine
# Optional: add an nginx config that serves index.html for spa routes
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build artifacts
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
