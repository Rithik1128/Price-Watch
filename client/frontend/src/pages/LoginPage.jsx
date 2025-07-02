import React from "react";
import "./LoginPage.css"; // CSS we'll update next

export default function LoginPage() {
  return (
    <div className="login-container">
      <div className="login-box">
        <h2 className="login-title">Welcome to <span>Price-Watch</span></h2>
        <p className="login-subtitle">Your personal price tracking assistant.</p>
        
        <button 
          className="google-button"
          onClick={() => {
            window.location.href = "http://localhost:8000/login/google";
          }}
        >
          <img
            src="https://www.svgrepo.com/show/475656/google-color.svg"
            alt="Google"
          />
          Sign in with Google
        </button>

        <p className="login-footer">Log in to start tracking products and save money!</p>
      </div>
    </div>
  );
}
