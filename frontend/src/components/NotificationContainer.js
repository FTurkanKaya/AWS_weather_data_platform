import React, { useState } from "react";

export default function NotificationContainer({
  userEmail,
  selectedCities,
  setSelectedCities,
  allCities,
  readOnly = false,
}) {
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleCheckboxChange = (city) => {
    if (readOnly) return;
    if (selectedCities.includes(city)) {
      setSelectedCities(selectedCities.filter((c) => c !== city));
    } else {
      setSelectedCities([...selectedCities, city]);
    }
  };

  const handleSubscribe = async () => {
    if (selectedCities.length === 0) {
      alert("Selecteer ten minste één stad.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(
        "https://nu2xfyytld.execute-api.eu-north-1.amazonaws.com/p/preferences",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: userEmail, selectedCities }),
        }
      );
      const data = await res.json();
      if (res.ok) {
        setIsSubscribed(true);
        alert(
          `Je ontvangt nu dagelijkse weerupdates voor: ${selectedCities.join(
            ", "
          )}.`
        );
      } else {
        console.error("Abonnement fout:", data.error);
        alert("Er is een fout opgetreden.");
      }
    } catch (err) {
      console.error("Subscription error:", err);
      alert("Er is een fout opgetreden.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="notification-container">
      <h3>📧 Dagelijkse meldingen</h3>
      <p>
        {isSubscribed
          ? `E-mailadres (${userEmail}) is nu geabonneerd op meldingen voor: ${selectedCities.join(
              ", "
            )}.`
          : "Wilt u dagelijkse e-mailmeldingen ontvangen voor de geselecteerde steden?"}
      </p>

      <div className="multi-city-checkboxes">
        {allCities.map((city) => (
          <div key={city} className="checkbox-item">
            <input
              type="checkbox"
              id={`city-${city}`}
              value={city}
              checked={selectedCities.includes(city)}
              onChange={() => handleCheckboxChange(city)}
              disabled={readOnly}
            />
            <label htmlFor={`city-${city}`}>{city}</label>
          </div>
        ))}
      </div>

      {!isSubscribed && !readOnly && (
        <button
          onClick={handleSubscribe}
          disabled={loading || selectedCities.length === 0}
        >
          {loading ? "Opslaan..." : "Ontvang e-mailmeldingen"}
        </button>
      )}
    </div>
  );
}



