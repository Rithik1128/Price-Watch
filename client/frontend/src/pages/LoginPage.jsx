import React from "react";
import { Link } from "react-router-dom";
import "./LoginPage.css"; // CSS we'll create next

export default function LoginPage() {
  return (
    <div className="login-container">
      <div className="login-box">
        <h2 className="login-title">Login to <span>PriceWatch</span></h2>

        <form className="login-form">
          <label>Email</label>
          <input type="email" placeholder="you@example.com" />

          <label>Password</label>
          <input type="password" placeholder="********" />

          <button type="submit">Login</button>
        </form>

        <div className="or-divider">OR</div>

        <button className="google-button"
          onClick={() => {
            window.location.href = "http://localhost:8000/login/google";
          }}
        >
          <img
            src="https://www.svgrepo.com/show/475656/google-color.svg"
            alt="Google"
          />
          Continue with Google
        </button>


        <p className="signup-link">
          Don’t have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
}
