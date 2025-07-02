import React, { useState } from 'react';
import './TrackProductForm.css';

const TrackProductForm = ({ onProductTracked }) => {
  const [productUrl, setProductUrl] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!productUrl) {
      setMessage({ type: 'error', text: 'Please enter a product URL.' });
      return;
    }

    setIsSubmitting(true);
    setMessage(null);

    try {
      const response = await fetch('http://localhost:8000/products', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ product_url: productUrl }),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || 'Failed to track product.');
      }

      if (result.status === 'added') {
        setMessage({ type: 'success', text: 'Product added successfully!' });
        onProductTracked(result); // Pass the new product data up
        setProductUrl(''); // Clear input
      } else if (result.status === 'exists') {
        setMessage({ type: 'info', text: 'You are already tracking this product.' });
      } else {
        setMessage({ type: 'error', text: result.error || 'An unknown error occurred.' });
      }

    } catch (err) {
      setMessage({ type: 'error', text: err.message });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="track-form">
        <input
          type="text"
          value={productUrl}
          onChange={(e) => setProductUrl(e.target.value)}
          placeholder="✏️ Enter Product URL"
          className="track-input"
        />
        <button type="submit" className="track-button" disabled={isSubmitting}>
          {isSubmitting ? '⏳ Tracking...' : '🔔 Start Tracking'}
        </button>
      </form>
      {message && (
        <p className={`form-message ${message.type}`}>{message.text}</p>
      )}
    </div>
  );
};

export default TrackProductForm;
