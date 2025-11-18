// src/config/awsConfig.js

const awsConfig = {
  Auth: {
    region: process.env.REACT_APP_AWS_REGION || "eu-north-1",

    userPoolId: process.env.REACT_APP_USER_POOL_ID || "eu-north-1_Lmrg8MXBO",

    userPoolWebClientId:
      process.env.REACT_APP_USER_POOL_CLIENT_ID || "673chm7bklp9fu44k6ll2flbk9",

    oauth: {
      domain:
        process.env.REACT_APP_COGNITO_DOMAIN ||
        "https://eu-north-1lmrg8mxbo.auth.eu-north-1.amazoncognito.com",

      scope: ["openid", "email", "profile"],

      redirectSignIn:
        process.env.REACT_APP_REDIRECT_SIGNIN || "http://localhost:3000/",

      redirectSignOut:
        process.env.REACT_APP_REDIRECT_SIGNOUT || "http://localhost:3000/",

      responseType: "code"
    }
  }
};

export default awsConfig;
