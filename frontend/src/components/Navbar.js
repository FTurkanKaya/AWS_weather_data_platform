import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Auth } from "aws-amplify";
import "../styles/Navbar.css";

export default function Navbar({ userName }) {
  const navigate = useNavigate();
  const [greeting, setGreeting] = useState("");

  const logout = async () => {
    try {
      await Auth.signOut();
      navigate("/login");
    } catch (err) {
      console.error("Logout error:", err);
    }
  };

  // Günün saatine göre selamlama belirle
    useEffect(() => {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) setGreeting("Goedemorgen");
    else if (hour >= 12 && hour < 18) setGreeting("Goedemiddag");
    else if (hour >= 18 && hour < 22) setGreeting("Goedenavond");
    else setGreeting("Goedenacht");
  }, []);

  return (
    <nav className="navbar-container">
      <div className="navbar-logo">
        <span>WeatherApp</span>
      </div>

      <div className="navbar-menu">
        {userName && (
          <div className="navbar-greeting">
            <span className="greeting-icon">🌤️</span>
            <span>{greeting}, {userName}!</span>
            <span className="welcome-text">Welkom</span>
          </div>
        )}
        <Link to="/dashboard" className="navbar-link">Dashboard</Link>
        <Link to="/profile" className="navbar-link">Profiel</Link>
        <button onClick={logout} className="navbar-logout">Uitloggen</button>
      </div>
    </nav>
  );
}

