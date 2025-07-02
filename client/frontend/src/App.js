// src/App.js
import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import HomePage from "./pages/HomePage";
import AddProductPage from "./pages/AddProductPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import DashboardPage from "./pages/DashboardPage";
import "./App.css";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch("http://localhost:8000/profile", {
          credentials: "include",
        });
        if (response.ok) {
          const data = await response.json();
          if (!data.error) {
            setUser(data);
          }
        }
      } catch (error) {
        console.error("Could not fetch profile:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleLogout = async () => {
    try {
      await fetch("http://localhost:8000/logout", { credentials: "include" });
      setUser(null);
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        <Header user={user} onLogout={handleLogout} />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/add" element={<AddProductPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route
              path="/dashboard"
              element={user ? <DashboardPage user={user} /> : <LoginPage />}
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
