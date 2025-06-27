import React from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="container">
      <Header title="Your Tracked Products" icon="📦" />
      <p className="subtitle">(This will later show products you're tracking)</p>
      <button className="primary-button" onClick={() => navigate("/add")}>
        ➕ Add New Product
      </button>
    </div>
  );
};

export default HomePage;
