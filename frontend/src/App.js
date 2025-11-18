import React from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import ProfilePage from "./pages/ProfilePage";
import LoginPage from "./pages/LoginPage";

export default function App() {
  const navigate = useNavigate();

  return (
    <Routes>
      <Route
        path="/login"
        element={<LoginPage onLoginSuccess={() => navigate("/dashboard")} />}
      />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/profile" element={<ProfilePage />} />
      <Route
        path="*"
        element={<LoginPage onLoginSuccess={() => navigate("/dashboard")} />}
      />
    </Routes>
  );
}


