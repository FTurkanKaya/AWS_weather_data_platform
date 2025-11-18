import React from "react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";

// Durumu hesaplayan fonksiyon (referans tablodaki eşik değerler)
const getStatus = (param, value) => {
  switch (param) {
    case "Fijnstof PM2.5":
      if (value <= 12) return { text: "Goed", color: "#34d399", advice: "Lucht is schoon" };
      if (value <= 35) return { text: "Gemiddeld", color: "#fbbf24", advice: "Luchtkwaliteit matig" };
      return { text: "Slecht", color: "#f87171", advice: "Binnen blijven indien gevoelig" };
    case "Fijnstof PM10":
      if (value <= 54) return { text: "Goed", color: "#34d399", advice: "Lucht is schoon" };
      if (value <= 154) return { text: "Gemiddeld", color: "#fbbf24", advice: "Matige vervuiling" };
      return { text: "Slecht", color: "#f87171", advice: "Vermijd buitenshuis activiteiten" };
    case "Stikstofdioxide (NO2)":
      if (value <= 40) return { text: "Goed", color: "#34d399", advice: "Lucht is schoon" };
      if (value <= 100) return { text: "Gemiddeld", color: "#fbbf24", advice: "Matige vervuiling" };
      return { text: "Slecht", color: "#f87171", advice: "Vermijd buitenshuis activiteiten" };
    case "Zwaveldioxide (SO2)":
      if (value <= 20) return { text: "Goed", color: "#34d399", advice: "Lucht is schoon" };
      if (value <= 75) return { text: "Gemiddeld", color: "#fbbf24", advice: "Matige vervuiling" };
      return { text: "Slecht", color: "#f87171", advice: "Binnen blijven indien mogelijk" };
    case "Ozon (O3)":
      if (value <= 100) return { text: "Goed", color: "#34d399", advice: "Lucht is schoon" };
      if (value <= 180) return { text: "Gemiddeld", color: "#fbbf24", advice: "Wees voorzichtig buiten" };
      return { text: "Slecht", color: "#f87171", advice: "Binnen blijven" };
    case "Koolmonoxide (CO)":
      if (value <= 4) return { text: "Goed", color: "#34d399", advice: "Veilig" };
      if (value <= 10) return { text: "Gemiddeld", color: "#fbbf24", advice: "Let op ventilatie" };
      return { text: "Slecht", color: "#f87171", advice: "Vermijd gesloten ruimtes" };
    case "Ammoniak (NH3)":
      if (value <= 200) return { text: "Goed", color: "#34d399", advice: "Geen risico" };
      if (value <= 400) return { text: "Gemiddeld", color: "#fbbf24", advice: "Let op gevoelige groepen" };
      return { text: "Slecht", color: "#f87171", advice: "Vermijd buitenactiviteiten" };
    default:
      return { text: "Onbekend", color: "#999", advice: "" };
  }
};

export default function WeatherRadar({ data }) {
  if (!data || data.length === 0) {
    return (
      <p style={{ textAlign: "center", marginTop: "2rem" }}>
        Selecteer een stad om de weersgegevens te bekijken.
      </p>
    );
  }

  const cityValues = data[0];

  const radarData = [
    { category: "Fijnstof PM2.5", value: cityValues.pm2_5 || 0 },
    { category: "Fijnstof PM10", value: cityValues.pm10 || 0 },
    { category: "Stikstofdioxide (NO2)", value: cityValues.no2 || 0 },
    { category: "Zwaveldioxide (SO2)", value: cityValues.so2 || 0 },
    { category: "Ozon (O3)", value: cityValues.o3 || 0 },
    { category: "Koolmonoxide (CO)", value: cityValues.co || 0 },
    { category: "Ammoniak (NH3)", value: cityValues.nh3 || 0 },
  ];

  // Tooltip componenti
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const { category, value } = payload[0].payload;
      const status = getStatus(category, value);

      return (
        <div style={{
          background: "#fff",
          border: "1px solid #ccc",
          padding: "10px",
          borderRadius: "8px",
          minWidth: "180px",
        }}>
          <p><strong>{category}</strong></p>
          <p>Waarde: <span style={{ color: status.color }}>{value}</span></p>
          <p>Status: <span style={{ color: status.color }}>{status.text}</span></p>
          <p>Advies: {status.advice}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="weather-graph-container">
      <h3 style={{ textAlign: "center", marginBottom: "1rem" }}>
        Luchtkwaliteitsradar - {cityValues.city_name}
      </h3>
      <ResponsiveContainer width="100%" height={350}>
        <RadarChart outerRadius="80%" data={radarData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="category" />
          <PolarRadiusAxis />
          <Radar
            name={cityValues.city_name}
            dataKey="value"
            stroke="#0072ff"
            fill="#0072ff"
            fillOpacity={0.6}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}



