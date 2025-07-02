import React, { useEffect, useState } from 'react';
import './DashboardPage.css';
import TrackProductForm from '../components/TrackProductForm';
import ProductCard from '../components/ProductCard';

const DashboardPage = ({ user }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch('http://localhost:8000/products', {
          credentials: 'include',
        });
        if (!response.ok) {
          throw new Error('Failed to fetch products.');
        }
        const data = await response.json();
        setProducts(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const handleProductTracked = (newProduct) => {
    setProducts((prevProducts) => [...prevProducts, newProduct]);
  };

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Welcome, {user.name}!</h1>
      <p className="dashboard-subtitle">Here are your tracked products.</p>

      <section id="track-product" className="track-section">
        <h2>Track a New Product</h2>
        <TrackProductForm onProductTracked={handleProductTracked} />
      </section>

      <section id="my-products" className="products-section">
        <h2>Your Tracked Products</h2>
        {loading && <p>Loading your products...</p>}
        {error && <p className="error-message">Error: {error}</p>}

        <div className="products-grid">
          {!loading && !error && products.length === 0 && (
            <p>
              You are not tracking any products yet. Use the form above to add
              one!
            </p>
          )}
          {products.map((product) => (
            <ProductCard key={product._id} product={product} />
          ))}
        </div>
      </section>
    </div>
  );
};

export default DashboardPage;
