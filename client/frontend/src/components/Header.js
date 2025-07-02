import React from "react";
import "./Header.css"; // We'll create this file next

const Header = ({ user, onLogout }) => {
  return (
    <header className="app-header">
      <div className="logo">
        <h1>🎯 Price-Watch</h1>
      </div>
      {user && (
        <nav className="navigation">
          <a href="#my-products">📦 My Products</a>
          <a href="#track-product">➕ Track</a>
        </nav>
      )}
      <div className="user-info">
        {user && (
          <>
            <img
              src={user.picture}
              alt={user.name}
              className="user-avatar"
            />
            <span className="user-name">{user.name}</span>
            <button onClick={onLogout} className="logout-button">
              Logout
            </button>
          </>
        )}
      </div>
    </header>
  );
};

export default Header;
