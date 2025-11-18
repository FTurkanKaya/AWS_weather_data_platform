import React from "react";

export default function ReferenceTable({ data }) {
  if (!data) return null;

  const rows = [
    { key: "air_quality_index", name: "Luchtkwaliteitsindex (AQI)" },
    { key: "pm2_5", name: "Fijnstof (PM2.5)" },
    { key: "pm10", name: "Stofdeeltjes (PM10)" },
    { key: "no2", name: "Stikstofdioxide (NO₂)" },
    { key: "so2", name: "Zwaveldioxide (SO₂)" },
    { key: "o3", name: "Ozon (O₃)" },
    { key: "co", name: "Koolmonoxide (CO)" },
    { key: "nh3", name: "Ammoniak (NH₃)" },
  ];

  const getColor = (key, value) => {
    if (value === null || value === undefined || value === 0) return "#f3f4f6"; // açık gri
    switch (key) {
      case "air_quality_index":
        if (value <= 2) return "#d1fae5"; // yeşil
        if (value <= 5) return "#fef3c7"; // sarı
        if (value <= 8) return "#fde68a"; // turuncu
        return "#fca5a5"; // kırmızı
      case "pm2_5":
        return value <= 25 ? "#d1fae5" : "#fca5a5";
      case "pm10":
        return value <= 50 ? "#d1fae5" : "#fca5a5";
      case "no2":
        return value <= 40 ? "#d1fae5" : "#fca5a5";
      case "so2":
        return value <= 20 ? "#d1fae5" : "#fca5a5";
      case "o3":
        return value <= 70 ? "#d1fae5" : "#fca5a5";
      case "co":
        return value <= 5 ? "#d1fae5" : "#fca5a5";
      case "nh3":
        return value <= 1 ? "#d1fae5" : "#fca5a5";
      default:
        return "#f3f4f6";
    }
  };

  const getAdvice = (key, value) => {
    if (value === null || value === undefined || value === 0) return "Geen gegevens beschikbaar."; // eksik veri
    switch (key) {
      case "air_quality_index":
        if (value <= 2) return "Lucht is schoon. Buiten zijn is prima.";
        if (value <= 5) return "Enkele risico's voor gevoelige personen. Overweeg een masker.";
        if (value <= 8) return "Luchtvervuiling hoog. Gevoelige personen binnen blijven, masker dragen.";
        return "Erg vervuild. Kinderen en ouderen binnen houden.";
      case "pm2_5":
        return value <= 25 ? "Normale waarden. Buitenactiviteiten veilig." : "Hoog. Luchtwegen kunnen geïrriteerd raken.";
      case "pm10":
        return value <= 50 ? "Veilige niveaus." : "Hoog. Veel stof en allergenen aanwezig, voorzichtig buiten.";
      case "no2":
        return value <= 40 ? "Normaal niveau." : "Hoog. Vermijd langdurige blootstelling buiten.";
      case "so2":
        return value <= 20 ? "Veilige waarden." : "Hoog. Kan irriterend zijn voor luchtwegen.";
      case "o3":
        return value <= 70 ? "Normaal niveau." : "Hoog. Vooral astmapatiënten voorzichtig.";
      case "co":
        return value <= 5 ? "Normale luchtkwaliteit." : "Hoog. Wees voorzichtig in gesloten ruimtes.";
      case "nh3":
        return value <= 1 ? "Normaal." : "Hoog. Geur en allergierisico aanwezig.";
      default:
        return "Geen advies beschikbaar.";
    }
  };

  return (
    <div className="reference-table-container">
      <h2 style={{ marginBottom: "15px", fontSize: "1.2rem" }}>🌿 Dagelijkse Luchtkwaliteitsadvies</h2>
      <table className="reference-table">
        <thead>
          <tr>
            <th>Parametre</th>
            <th>Waarde</th>
            <th>Advies</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => {
            const value = data[row.key] ?? 0;
            const bgColor = getColor(row.key, value);
            const advice = getAdvice(row.key, value);
            return (
              <tr key={row.key} style={{ backgroundColor: bgColor }}>
                <td>{row.name}</td>
                <td>{value}</td>
                <td>{advice}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

