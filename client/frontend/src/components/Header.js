import React from "react";

const Header = ({ title, icon }) => {
  return (
    <div className="header">
      <h1>{icon} {title}</h1>
    </div>
  );
};

export default Header;
