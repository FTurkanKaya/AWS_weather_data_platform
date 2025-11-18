import React, { useEffect, useState } from "react";
import { Auth } from "aws-amplify";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import WeatherCard from "../components/WeatherCard";
import WeatherRadar from "../components/WeatherRadar";
import ReferenceTable from "../components/ReferenceTable";
import NotificationContainer from "../components/NotificationContainer";
import Clock from "../components/Clock";
import "../styles/dashboard.css";
import { FaMapMarkerAlt } from "react-icons/fa";

export default function DashboardPage() {
  const navigate = useNavigate();
  const [weatherData, setWeatherData] = useState([]);
  const [selectedCity, setSelectedCity] = useState("");
  const [allCities, setAllCities] = useState([]);
  const [userName, setUserName] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [selectedCities, setSelectedCities] = useState([]);
  const [selectedDate, setSelectedDate] = useState(
    new Date().toISOString().split("T")[0]
  );

  // Kullanıcı bilgilerini getir
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await Auth.currentAuthenticatedUser();
        const name = user.attributes.name || user.username;
        setUserName(name);
        setUserEmail(user.attributes.email);
      } catch (err) {
        console.error("User fetch error:", err);
      }
    };
    fetchUser();
  }, []);

  // Hava durumu verilerini getir
  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        const date = new Date(selectedDate);
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();

        const response = await fetch(
          `https://nu2xfyytld.execute-api.eu-north-1.amazonaws.com/p/weather?year=${year}&month=${month}&day=${day}`
        );
        const data = await response.json();

        if (!Array.isArray(data)) {
          console.error("Beklenmeyen veri:", data);
          return;
        }

        const normalized = data.map((item) => ({
          ...item,
          air_quality_index: parseFloat(item.air_quality_index) || 0,
          co: parseFloat(item.co) || 0,
          no: parseFloat(item.no) || 0,
          no2: parseFloat(item.no2) || 0,
          o3: parseFloat(item.o3) || 0,
          so2: parseFloat(item.so2) || 0,
          nh3: parseFloat(item.nh3) || 0,
          pm2_5: parseFloat(item.pm2_5) || 0,
          pm10: parseFloat(item.pm10) || 0,
        }));

        setWeatherData(normalized);

        const cities = [...new Set(normalized.map((d) => d.city_name))];
        setAllCities(cities);

        if (cities.length > 0 && !cities.includes(selectedCity)) {
          setSelectedCity(cities[0]);
        }
      } catch (error) {
        console.error("Weather fetch error:", error);
      }
    };
    fetchWeatherData();
  }, [selectedDate]);

  const filteredData = selectedCity
    ? weatherData.filter((item) => item.city_name === selectedCity)
    : [];

  return (
    <div>
      <Navbar userName={userName} />
      <div className="dashboard-container">
        {/* Şehir + Tarih Seçimi */}
        <div className="selector-container">
          <div className="city-selector-section">
            <h2 className="section-title">
              <FaMapMarkerAlt style={{ color: "#a80000" }} />
              Selecteer uw stad
            </h2>
            <div className="city-selector">
              {allCities.length === 0 ? (
                <p>Steden laden...</p>
              ) : (
                <select
                  value={selectedCity}
                  onChange={(e) => setSelectedCity(e.target.value)}
                >
                  {allCities.map((city) => (
                    <option key={city} value={city}>
                      {city}
                    </option>
                  ))}
                </select>
              )}
            </div>
          </div>

          {/* Tarih Seçici */}
          <div className="date-selector">
            <button
              onClick={() => {
                const prev = new Date(selectedDate);
                prev.setDate(prev.getDate() - 1);
                setSelectedDate(prev.toISOString().split("T")[0]);
              }}
            >
              ◀ Vorige dag
            </button>

            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              max={new Date().toISOString().split("T")[0]}
            />

            <button
              onClick={() => {
                const next = new Date(selectedDate);
                next.setDate(next.getDate() + 1);
                if (next <= new Date()) {
                  setSelectedDate(next.toISOString().split("T")[0]);
                }
              }}
            >
              Volgende dag ▶
            </button>
          </div>
        </div>

        {/* Hava Kartları */}
        {filteredData.length > 0 && (
          <div className="weather-cards">
            {filteredData.map((data) => (
              <WeatherCard key={data.city_name} data={data} />
            ))}
          </div>
        )}

        {/* Radar ve Tablo */}
        {filteredData.length > 0 && (
          <div className="dashboard-bottom">
            <div className="weather-graph-container">
              <WeatherRadar data={filteredData} />
            </div>
            <div className="reference-table-container">
              <ReferenceTable data={filteredData[0]} />
            </div>
          </div>
        )}

        {/* Bildirim & Saat */}
        <div className="notification-section">
          <NotificationContainer
            userEmail={userEmail}
            selectedCities={selectedCities}
            setSelectedCities={setSelectedCities}
            allCities={allCities}
            selectCityText="Selecteer steden voor meldingen"
          />
          <div className="bottom-clock-section">
            <Clock />
          </div>
        </div>
      </div>
    </div>
  );
}
