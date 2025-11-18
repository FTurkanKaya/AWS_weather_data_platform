const awsConfig = {
  Auth: {
    region: "eu-north-1",
    userPoolId: "eu-north-1_Lmrg8MXBO",
    userPoolWebClientId: "673chm7bklp9fu44k6ll2flbk9",
    oauth: {
      domain: "https://eu-north-1lmrg8mxbo.auth.eu-north-1.amazoncognito.com", 
      scope: ["openid", "email", "profile"],
      redirectSignIn: "http://localhost:3000/",
      redirectSignOut: "http://localhost:3000/",
      responseType: "code"
    }
  }
};

export default awsConfig;


