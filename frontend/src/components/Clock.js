// src/components/Clock.js
import React, { useEffect, useState } from "react";
import "../styles/Clock.css";

export default function Clock() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  const options = {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    weekday: "short",
    day: "2-digit",
    month: "short",
    year: "numeric",
    timeZone: "Europe/Paris"
  };

  const formattedTime = time.toLocaleString('nl-NL', options);

  return <div className="time-container">{formattedTime}</div>;
}
