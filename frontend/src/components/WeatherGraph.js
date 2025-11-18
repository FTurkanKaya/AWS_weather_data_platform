import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from "recharts";

export default function WeatherGraph({ data }) {
  console.log("WeatherGraph received:", data);

  const graphData = data.map(item => ({
    city: item.city_name,
    havaKalitesi: parseFloat(item.air_quality_index) || 0,
    karbonmonoksit: parseFloat(item.co) || 0,
    azotDioksit: parseFloat(item.no2) || 0,
  }));

  console.log("Graph data processed:", graphData);

  return (
    <LineChart width={600} height={300} data={graphData}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="city" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="havaKalitesi" stroke="#8884d8" name="Luchtkwaliteit" />
      <Line type="monotone" dataKey="karbonmonoksit" stroke="#82ca9d" name="Koolmonoxide (CO)" />
      <Line type="monotone" dataKey="azotDioksit" stroke="#ffc658" name="Stikstofdioxide (NO₂)" />

    </LineChart>
  );
}

