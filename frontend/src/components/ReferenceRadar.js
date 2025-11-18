import React from "react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
} from "recharts";

// Renkleri tablo ile eşle
const getColor = (param, value) => {
  switch (param) {
    case "PM2.5":
      if (value <= 12) return "#34d399"; // yeşil
      if (value <= 35) return "#fbbf24"; // sarı
      return "#f87171"; // kırmızı
    case "PM10":
      if (value <= 54) return "#34d399";
      if (value <= 154) return "#fbbf24";
      return "#f87171";
    case "NO2":
      if (value <= 40) return "#34d399";
      if (value <= 100) return "#fbbf24";
      return "#f87171";
    case "SO2":
      if (value <= 20) return "#34d399";
      if (value <= 75) return "#fbbf24";
      return "#f87171";
    case "O3":
      if (value <= 100) return "#34d399";
      if (value <= 180) return "#fbbf24";
      return "#f87171";
    case "CO":
      if (value <= 4) return "#34d399";
      if (value <= 10) return "#fbbf24";
      return "#f87171";
    case "NH3":
      if (value <= 200) return "#34d399";
      if (value <= 400) return "#fbbf24";
      return "#f87171";
    default:
      return "#34d399";
  }
};

export default function ReferenceRadar({ data }) {
  if (!data) return null;

  const radarData = [
    { category: "PM2.5", value: data.pm2_5 ?? 0 },
    { category: "PM10", value: data.pm10 ?? 0 },
    { category: "NO2", value: data.no2 ?? 0 },
    { category: "SO2", value: data.so2 ?? 0 },
    { category: "O3", value: data.o3 ?? 0 },
    { category: "CO", value: data.co ?? 0 },
    { category: "NH3", value: data.nh3 ?? 0 },
  ];

  return (
    <div className="reference-radar">
      <h3 className="text-center mb-2 font-semibold text-gray-700">
        🌍 Luchtkwaliteitsgrafiek
      </h3>
      <ResponsiveContainer width="100%" height={350}>
        <RadarChart outerRadius="80%" data={radarData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="category" />
          <PolarRadiusAxis />
          {radarData.map((item) => (
            <Radar
              key={item.category}
              name={item.category}
              dataKey={() => item.value}
              stroke={getColor(item.category, item.value)}
              fill={getColor(item.category, item.value)}
              fillOpacity={0.5}
            />
          ))}
          <Legend />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
