import React, { useState, useEffect } from 'react';
import { productService, cartService } from '../../services/sales';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [addingToCart, setAddingToCart] = useState(null);
  const [cartMessage, setCartMessage] = useState('');

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const productsData = await productService.getProducts();
      setProducts(productsData);
    } catch (error) {
      console.error('Error cargando productos:', error);
    } finally {
      setLoading(false);
    }
  };

  const categories = [...new Set(products.map(product => product.categoria_nombre))];

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.nombre.toLowerCase().includes(filter.toLowerCase()) ||
                         product.descripcion?.toLowerCase().includes(filter.toLowerCase());
    const matchesCategory = !categoryFilter || product.categoria_nombre === categoryFilter;
    
    return matchesSearch && matchesCategory;
  });

  const addToCart = async (productId, productName) => {
    setAddingToCart(productId);
    setCartMessage('');
    
    try {
      await cartService.addToCart(productId, 1);
      setCartMessage(`✅ "${productName}" agregado al carrito`);
      
      // Limpiar mensaje después de 3 segundos
      setTimeout(() => setCartMessage(''), 3000);
    } catch (error) {
      setCartMessage(`❌ ${error.response?.data?.error || 'Error agregando al carrito'}`);
    } finally {
      setAddingToCart(null);
    }
  };

  const viewCart = () => {
    window.location.href = '/carrito';
  };

  if (loading) {
    return <div className="loading">Cargando productos...</div>;
  }

  return (
    <div className="product-list-client">
      <div className="products-header">
        <h2>Catálogo de Productos</h2>
        
        {cartMessage && (
          <div className={`cart-message ${cartMessage.includes('✅') ? 'success' : 'error'}`}>
            {cartMessage}
            {cartMessage.includes('✅') && (
              <button onClick={viewCart} className="view-cart-btn">
                Ver Carrito
              </button>
            )}
          </div>
        )}
      </div>
      
      <div className="filters">
        <div className="search-filter">
          <input
            type="text"
            placeholder="Buscar productos..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          />
        </div>
        
        <div className="category-filter">
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
          >
            <option value="">Todas las categorías</option>
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
        </div>
      </div>

      {filteredProducts.length === 0 ? (
        <div className="no-products">
          <p>No se encontraron productos</p>
        </div>
      ) : (
        <div className="products-grid">
          {filteredProducts.map(product => (
            <div key={product.id} className="product-card">
              <div className="product-header">
                <h3>{product.nombre}</h3>
                <span className="price">${product.precio}</span>
              </div>
              
              <div className="product-category">
                {product.categoria_nombre}
              </div>
              
              <p className="product-description">
                {product.descripcion || 'Sin descripción'}
              </p>
              
              <div className="product-stock">
                <span className={`stock-badge ${product.stock > 10 ? 'high' : product.stock > 0 ? 'low' : 'out'}`}>
                  {product.stock > 10 ? 'Disponible' : product.stock > 0 ? 'Últimas unidades' : 'Agotado'}
                </span>
                <span className="stock-count">{product.stock} unidades</span>
              </div>

              <div className="product-actions">
                <button 
                  className={`add-to-cart-btn ${product.stock === 0 ? 'disabled' : ''}`}
                  onClick={() => addToCart(product.id, product.nombre)}
                  disabled={product.stock === 0 || addingToCart === product.id}
                >
                  {addingToCart === product.id ? 'Agregando...' : 
                   product.stock === 0 ? 'Agotado' : 'Agregar al Carrito'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProductList;