import React from "react";

export default function MultiCitySelector({ cities, selectedCities, onChange }) {
  const handleChange = (e) => {
    const values = Array.from(e.target.selectedOptions, (opt) => opt.value);
    onChange(values);
  };

  return (
    <div className="multi-city-selector">
      <label className="block mb-2 font-semibold">Şehir(ler) Seç:</label>
      <select
        multiple
        value={selectedCities}
        onChange={handleChange}
        className="border rounded px-3 py-3 w-full text-lg"
        size={5}
      >
        {cities.map((city) => (
          <option key={city} value={city}>
            {city}
          </option>
        ))}
      </select>
    </div>
  );
}
