import React, { useEffect, useState } from "react";
import { CognitoUserPool } from "amazon-cognito-identity-js";
import awsConfig from "../aws-exports";
import "../styles/profile.css";
import Navbar from "../components/Navbar";
import Clock from "../components/Clock";

const userPool = new CognitoUserPool({
  UserPoolId: awsConfig.Auth.userPoolId,
  ClientId: awsConfig.Auth.userPoolWebClientId,
});

export default function ProfilePage() {
  const [preferences, setPreferences] = useState([]);
  const [loading, setLoading] = useState(true);
  const [userEmail, setUserEmail] = useState("");
  const [profile, setProfile] = useState({});
  const [userName, setUserName] = useState("");

  const API_URL = "https://nu2xfyytld.execute-api.eu-north-1.amazonaws.com/p/profielpage";

  useEffect(() => {
    const fetchData = async () => {
      const user = userPool.getCurrentUser();
      if (!user) {
        setLoading(false);
        return;
      }

      user.getSession(async (err, session) => {
        if (err || !session) {
          setLoading(false);
          return;
        }

        const email = session.getIdToken().payload.email;
        setUserEmail(email);

        const name =
          session.getIdToken().payload.name ||
          session.getIdToken().payload.given_name ||
          session.getIdToken().payload["cognito:username"];
        setUserName(name);

        try {
          // Kullanıcı tercihleri
          const resPref = await fetch(
            `https://nu2xfyytld.execute-api.eu-north-1.amazonaws.com/p/preferences?email=${email}`
          );
          const dataPref = await resPref.json();
          setPreferences(dataPref.preferences || []);

          // Profil bilgileri
          const resProfile = await fetch(`${API_URL}?email=${email}`);
          if (!resProfile.ok) throw new Error(`HTTP ${resProfile.status}`);
          const dataProfile = await resProfile.json();
          setProfile({
            ...dataProfile.user,
            phone_number: dataProfile.user.phone_number || "",
          });
        } catch (error) {
          console.error("Fetch hatası:", error);
        } finally {
          setLoading(false);
        }
      });
    };

    fetchData();
  }, []);

  const handleDelete = async (city) => {
    if (!window.confirm(`Weet je zeker dat je ${city} wilt verwijderen?`)) return;

    try {
      const res = await fetch(
        `https://nu2xfyytld.execute-api.eu-north-1.amazonaws.com/p/DELETEuserpreferences?email=${userEmail}&city=${encodeURIComponent(city)}`,
        { method: "DELETE" }
      );

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      await res.json();
      setPreferences((prev) => prev.filter((pref) => pref.city !== city));
    } catch (error) {
      console.error("Verwijderfout:", error);
      alert("Er is een fout opgetreden bij het verwijderen van de stad.");
    }
  };

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleUpdateAll = async () => {
    try {
      const updateData = { ...profile, email: userEmail };
      const res = await fetch(API_URL, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updateData),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      alert(data.message || "Profiel succesvol bijgewerkt!");
    } catch (error) {
      console.error("Updatefout:", error);
      alert("Er is een fout opgetreden bij het bijwerken van het profiel.");
    }
  };

  if (loading) return <p>Laden...</p>;

  return (
    <>
      <Navbar userName={userName} />

      <div
        className="profile-page"
        style={{ display: "flex", gap: "40px", paddingTop: "80px", paddingBottom: "60px" }}
      >
        {/* Sol: Şehir tercihleri */}
        <div className="profile-container" style={{ flex: 1 }}>
          <h2>Gekozen steden</h2>
          {preferences.length === 0 ? (
            <p>Er zijn nog geen steden geselecteerd.</p>
          ) : (
            <div className="city-boxes">
              {preferences.map((pref) => (
                <div key={pref.city} className="city-box">
                  {pref.city}
                  <button
                    className="remove-btn"
                    onClick={() => handleDelete(pref.city)}
                    title="Verwijderen"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Sağ: Profil bilgileri */}
        <div className="profile-container" style={{ flex: 1 }}>
          <h2>Uw profielgegevens</h2>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleUpdateAll();
            }}
          >
            {Object.keys(profile).map((key) => {
              // Telefon alanını özel placeholder ve pattern ile göster
              if (key === "phone_number") {
                return (
                  <div
                    key={key}
                    style={{ marginBottom: "12px", display: "flex", alignItems: "center", gap: "8px" }}
                  >
                    <label style={{ width: "120px", textTransform: "capitalize" }}>
                      Telefoon:
                    </label>
                    <input
                      type="tel"
                      name={key}
                      value={profile[key] || ""}
                      onChange={handleChange}
                      placeholder="+31xxxxxxxxx"
                      pattern="^\+\d{1,15}$"
                      title="Het nummer moet beginnen met '+' en cijfers bevatten"
                    />
                  </div>
                );
              }

              return (
                <div
                  key={key}
                  style={{ marginBottom: "12px", display: "flex", alignItems: "center", gap: "8px" }}
                >
                  <label style={{ width: "120px", textTransform: "capitalize" }}>
                    {key === "first_name"
                      ? "Voornaam"
                      : key === "last_name"
                      ? "Achternaam"
                      : key === "email"
                      ? "E-mail"
                      : key.replace("_", " ")}
                    :
                  </label>
                  <input
                    type={key === "email" ? "email" : "text"}
                    name={key}
                    value={profile[key] || ""}
                    onChange={handleChange}
                    disabled={key === "email"}
                  />
                </div>
              );
            })}
            <button type="submit" className="add-city-button">
              Profiel bijwerken
            </button>
          </form>
        </div>
      </div>

      <Clock />
    </>
  );
}


