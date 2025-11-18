import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { Amplify } from "aws-amplify";  // ⚠️ Düzeltildi
import awsconfig from "./aws-exports";
import "./styles/index.css";

// Amplify configure
Amplify.configure(awsconfig);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);




