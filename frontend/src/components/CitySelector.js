import React from "react";

export default function CitySelector({ cities, selectedCity, onChange }) {
  return (
    <div className="single-city-selector">
      <label className="block mb-1 font-semibold">Şehir Seçin:</label>
      <select
        value={selectedCity}
        onChange={(e) => onChange(e.target.value)}
        className="border rounded px-3 py-2 w-full"
      >
        <option value="">-- Şehir Seçin --</option>
        {cities.map((city) => (
          <option key={city} value={city}>
            {city}
          </option>
        ))}
      </select>
    </div>
  );
}


