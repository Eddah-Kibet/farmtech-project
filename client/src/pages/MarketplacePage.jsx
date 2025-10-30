import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import ProductCard from '../components/ProductCard';
import ReviewForm from '../components/ReviewForm';
import './MarketplacePage.css';

const MarketplacePage = () => {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showReviewForm, setShowReviewForm] = useState(false);

  React.useEffect(() => {
    if (!currentUser) {
      navigate('/login');
    }
  }, [currentUser, navigate]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get('/products');
        setProducts(response.data);
        setFilteredProducts(response.data);
      } catch (error) {
        console.error('Error fetching products:', error);
        setProducts([]);
        setFilteredProducts([]);
      }
    };
    fetchProducts();
  }, []);

  
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('product');
    const review = urlParams.get('review');

    if (productId && review === 'true') {
      const product = products.find(p => p.id === parseInt(productId));
      if (product) {
        setSelectedProduct(product);
        setShowReviewForm(true);
        
        window.scrollTo(0, 0);
      }
    }
  }, [products]);

  useEffect(() => {
    let filtered = products;

    
    if (selectedCategory !== 'All') {
      filtered = filtered.filter(product => product.category === selectedCategory);
    }

    
    if (searchTerm) {
      filtered = filtered.filter(product =>
        product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredProducts(filtered);
  }, [products, selectedCategory, searchTerm]);

  if (!currentUser) {
    return null;
  }

  const handleReviewSubmitted = () => {
    setShowReviewForm(false);
    setSelectedProduct(null);
    
    navigate('/marketplace', { replace: true });
  };

  return (
    <div className="marketplace-page">
      <div className="marketplace-container">
        <h1>Marketplace</h1>
        <p>Browse and shop for fresh farm produce</p>

        {}
        {showReviewForm && selectedProduct && (
          <div className="review-modal">
            <div className="review-modal-content">
              <div className="review-modal-header">
                <h2>Review {selectedProduct.name}</h2>
                <button
                  className="close-modal-btn"
                  onClick={() => {
                    setShowReviewForm(false);
                    setSelectedProduct(null);
                    navigate('/marketplace', { replace: true });
                  }}
                >
                  ×
                </button>
              </div>
              <div className="review-modal-body">
                <div className="product-preview">
                  <img src={selectedProduct.image} alt={selectedProduct.name} />
                  <div className="product-details">
                    <h3>{selectedProduct.name}</h3>
                    <p>{selectedProduct.description}</p>
                    <p className="price">KSh {selectedProduct.price.toLocaleString()}</p>
                  </div>
                </div>
                <ReviewForm
                  productId={selectedProduct.id}
                  farmerId={selectedProduct.farmer_id}
                  onReviewSubmitted={handleReviewSubmitted}
                />
              </div>
            </div>
          </div>
        )}

        {}
        <div className="marketplace-controls">
          <div className="search-bar">
            <input
              type="text"
              placeholder="Search products..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
          <div className="category-filter">
            <label htmlFor="category-select" className="category-label">Category:</label>
            <select
              id="category-select"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="category-select"
            >
              <option value="All">All Categories</option>
              <option value="Vegetables">Vegetables</option>
              <option value="Fruits">Fruits</option>
              <option value="Dairy">Dairy</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>

        {}
        <div className="products-grid">
          {filteredProducts.length === 0 ? (
            <div className="no-products">
              <p>No products found matching your criteria.</p>
            </div>
          ) : (
            filteredProducts.map(product => (
              <ProductCard key={product.id} product={product} />
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default MarketplacePage;
