import React, { useState, useEffect } from 'react';
import { saleService, productService, clientService } from '../../services/sales';

const SaleRegister = () => {
  const [formData, setFormData] = useState({
    cliente: '',
    producto: '',
    cantidad: 1,
    precio_unitario: 0
  });
  const [products, setProducts] = useState([]);
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [selectedProduct, setSelectedProduct] = useState(null);

  useEffect(() => {
    loadProducts();
    loadClients();
  }, []);

  const loadProducts = async () => {
    try {
      const productsData = await productService.getProducts();
      setProducts(productsData);
    } catch (error) {
      console.error('Error cargando productos:', error);
      setMessage('Error cargando productos');
    }
  };

  const loadClients = async () => {
    try {
      const clientsData = await clientService.getClients();
      setClients(clientsData);
    } catch (error) {
      console.error('Error cargando clientes:', error);
      setMessage('Error cargando clientes');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    if (name === 'producto') {
      const product = products.find(p => p.id == value);
      setSelectedProduct(product);
      setFormData(prev => ({
        ...prev,
        [name]: value,
        precio_unitario: product ? product.precio : 0
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      await saleService.createSale(formData);
      setMessage('✅ Venta registrada exitosamente');
      setFormData({
        cliente: '',
        producto: '',
        cantidad: 1,
        precio_unitario: 0
      });
      setSelectedProduct(null);
      
      // Recargar productos para actualizar stock
      loadProducts();
    } catch (error) {
      setMessage(`❌ Error: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const total = formData.cantidad * formData.precio_unitario;

  return (
    <div className="sale-register">
      <h2>Registrar Nueva Venta</h2>
      
      <form onSubmit={handleSubmit} className="sale-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="cliente">Cliente:</label>
            <select
              id="cliente"
              name="cliente"
              value={formData.cliente}
              onChange={handleChange}
              required
              disabled={loading}
            >
              <option value="">Seleccionar cliente</option>
              {clients.map(client => (
                <option key={client.id} value={client.id}>
                  {client.nombre} - {client.email}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="producto">Producto:</label>
            <select
              id="producto"
              name="producto"
              value={formData.producto}
              onChange={handleChange}
              required
              disabled={loading}
            >
              <option value="">Seleccionar producto</option>
              {products.map(product => (
                <option key={product.id} value={product.id}>
                  {product.nombre} - ${product.precio} (Stock: {product.stock})
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="cantidad">Cantidad:</label>
            <input
              type="number"
              id="cantidad"
              name="cantidad"
              value={formData.cantidad}
              onChange={handleChange}
              min="1"
              max={selectedProduct ? selectedProduct.stock : 1}
              required
              disabled={loading}
            />
            {selectedProduct && (
              <small className="stock-info">
                Stock disponible: {selectedProduct.stock} unidades
              </small>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="precio_unitario">Precio Unitario:</label>
            <input
              type="number"
              id="precio_unitario"
              name="precio_unitario"
              value={formData.precio_unitario}
              onChange={handleChange}
              step="0.01"
              min="0"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label>Total:</label>
            <div className="total-amount">
              ${total.toFixed(2)}
            </div>
          </div>
        </div>

        {message && (
          <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>
            {message}
          </div>
        )}

        <button 
          type="submit" 
          disabled={loading || !formData.cliente || !formData.producto}
          className="submit-button"
        >
          {loading ? 'Registrando...' : 'Registrar Venta'}
        </button>
      </form>

      {selectedProduct && (
        <div className="product-info">
          <h4>Información del Producto Seleccionado:</h4>
          <p><strong>Nombre:</strong> {selectedProduct.nombre}</p>
          <p><strong>Categoría:</strong> {selectedProduct.categoria_nombre}</p>
          <p><strong>Descripción:</strong> {selectedProduct.descripcion}</p>
          <p><strong>Stock disponible:</strong> {selectedProduct.stock} unidades</p>
        </div>
      )}
    </div>
  );
};

export default SaleRegister;