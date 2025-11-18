import React, { useState } from "react";
import { Auth } from "aws-amplify";
import "../styles/login.css";

export default function LoginPage({ onLoginSuccess }) {
  const [formType, setFormType] = useState("signIn");
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    email: "",
    name: "",
    family_name: "",
    phone_number: "",
  });
  const [confirmationCode, setConfirmationCode] = useState("");
  const [phoneError, setPhoneError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === "phone_number") {
      if (!/^\+\d{1,15}$/.test(value)) {
        setPhoneError("Het nummer moet beginnen met '+' en cijfers bevatten");
      } else {
        setPhoneError("");
      }
    }
    setFormData({ ...formData, [name]: value });
  };

  const signUp = async () => {
    if (phoneError) {
      alert("Voer een geldig telefoonnummer in dat begint met '+'");
      return;
    }
    try {
      const { username, password, email, name, family_name, phone_number } = formData;
      await Auth.signUp({
        username,
        password,
        attributes: { email, name, family_name, phone_number },
      });
      alert("Registratie succesvol! Voer de bevestigingscode in.");
      setFormType("confirmSignUp");
    } catch (err) {
      alert(err.message);
    }
  };

  const confirmSignUp = async () => {
    try {
      await Auth.confirmSignUp(formData.username, confirmationCode);
      alert("Bevestiging voltooid! Je kunt nu inloggen.");
      setFormType("signIn");
    } catch (err) {
      alert(err.message);
    }
  };

  const signIn = async () => {
    try {
      await Auth.signIn(formData.username, formData.password);
      alert("Succesvol ingelogd!");
      onLoginSuccess();
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="login-page">
      <div className="login-form-container">
        {formType === "signIn" && (
          <>
            <h2>Inloggen</h2>
            <input name="username" placeholder="Gebruikersnaam" onChange={handleChange} className="input" />
            <input name="password" type="password" placeholder="Wachtwoord" onChange={handleChange} className="input" />
            <button onClick={signIn} className="btn-primary">Inloggen</button>
            <p onClick={() => setFormType("signUp")} className="link">Account aanmaken</p>
          </>
        )}

        {formType === "signUp" && (
          <>
            <h2>Nieuw account</h2>
            <input name="username" placeholder="Gebruikersnaam" onChange={handleChange} className="input" />
            <input name="email" placeholder="E-mail" onChange={handleChange} className="input" />
            <input name="password" type="password" placeholder="Wachtwoord" onChange={handleChange} className="input" />
            <input name="name" placeholder="Voornaam" onChange={handleChange} className="input" />
            <input name="family_name" placeholder="Achternaam" onChange={handleChange} className="input" />
            <div style={{ display: "flex", flexDirection: "column" }}>
              <input
                name="phone_number"
                placeholder="+31xxxxxxxxx"
                value={formData.phone_number}
                onChange={handleChange}
                className="input"
              />
              {phoneError && <span style={{ color: "red", fontSize: "0.8em", marginTop: "2px" }}>{phoneError}</span>}
            </div>
            <button onClick={signUp} className="btn-primary">Registreren</button>
            <p onClick={() => setFormType("signIn")} className="link">Heb je al een account?</p>
          </>
        )}

        {formType === "confirmSignUp" && (
          <>
            <h2>Bevestigingscode</h2>
            <input placeholder="Code" onChange={(e) => setConfirmationCode(e.target.value)} className="input" />
            <button onClick={confirmSignUp} className="btn-primary">Bevestigen</button>
          </>
        )}
      </div>
    </div>
  );
}

