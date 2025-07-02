import React from 'react';
import './ProductCard.css';

const ProductCard = ({ product }) => {
  const { title, currentPrice, targetPrice, viewLink, lastUpdated } = product;

  return (
    <div className="product-card">
      <h3 className="product-title">{title}</h3>
      <div className="price-info">
        <p><strong>Current Price:</strong> <span className="current-price">{currentPrice}</span></p>
        {targetPrice && <p><strong>Target Price:</strong> <span className="target-price">{targetPrice}</span></p>}
      </div>
      <div className="card-footer">
        <p className="last-updated">Last updated: {lastUpdated}</p>
        <div className="card-actions">
          <a href={viewLink} target="_blank" rel="noopener noreferrer" className="action-btn view-btn">View</a>
          <button className="action-btn edit-btn">✏️</button>
          <button className="action-btn delete-btn">🗑️</button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
