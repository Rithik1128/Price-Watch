import React from "react";
import Header from "../components/Header";

const AddProduct = () => {
  return (
    <div className="container">
      <Header title="Add New Product" icon="🛒" />
      <form className="form">
        <label>
          Product URL:
          <input type="text" placeholder="https://example.com/product" />
        </label>
        <label>
          Notification Type:
          <select>
            <option>Below Custom Range</option>
            <option>Any Lower Price</option>
            <option>Below Fixed Price</option>
          </select>
        </label>
        <label>
          Price Range / Value:
          <input type="number" placeholder="e.g. 15000" />
        </label>
        <button className="primary-button" type="submit">Track Product</button>
      </form>
    </div>
  );
};

export default AddProduct;
