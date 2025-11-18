import React from "react";

export default function WeatherCard({ data }) {
  // Allerjen seviyesini hesaplayan fonksiyon
  const calculateAllergenLevel = (data) => {
    const { pm2_5, pm10, o3, no2 } = data;

    // Normalize ederek skor hesapla
    const score =
      (pm2_5 / 50) + // PM2.5 normalize
      (pm10 / 50) +   // PM10 normalize
      (o3 / 100) +    // O3 normalize
      (no2 / 100);    // NO2 normalize

    // Halk dilinde sınıflandır
    if (score <= 2) return "Lage allergieniveau";
    if (score <= 5) return "Gemiddeld allergieniveau";
    if (score <= 8) return "Hoog allergieniveau";
    return "Zeer hoog allergieniveau";
  };

  const allergenLevel = calculateAllergenLevel(data);

  return (
    <div className="weather-card">
      <h2>{data.city_name}</h2>
      <p><strong>Air Quality Index (AQI):</strong> {data.air_quality_index}</p>
      <p style={{ marginTop: "10px", fontWeight: "bold", color: "#d97706" }}>
        Allergieniveau: {allergenLevel}
      </p>
    </div>
  );
}
