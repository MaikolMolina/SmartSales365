import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../models/cart_item.dart';
import '../../services/cart_service.dart';
import '../../widgets/cart_icon.dart';

class CartScreen extends StatefulWidget {
  @override
  _CartScreenState createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  List<CartItem> _cartItems = [];
  double _totalPrice = 0;
  bool _loading = true;
  String _error = '';

  @override
  void initState() {
    super.initState();
    _loadCart();
  }

  Future<void> _loadCart() async {
    try {
      final cartResponse = await CartService().getCart();
      setState(() {
        _cartItems = cartResponse.items;
        _totalPrice = cartResponse.resumen.totalPrecio;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }

  Future<void> _updateQuantity(CartItem item, int newQuantity) async {
    if (newQuantity < 1) return;

    try {
      await CartService().updateCartItem(item.id, newQuantity);
      await _loadCart(); // Recargar el carrito
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Cantidad actualizada')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  Future<void> _removeItem(int itemId) async {
    try {
      await CartService().removeFromCart(itemId);
      await _loadCart(); // Recargar el carrito
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Producto eliminado del carrito')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error eliminando producto: $e')),
      );
    }
  }

  Future<void> _clearCart() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Vaciar Carrito'),
        content: Text('¿Estás seguro de que quieres vaciar todo el carrito?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: Text('Cancelar'),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(true),
            child: Text('Vaciar'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      try {
        await CartService().clearCart();
        await _loadCart();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Carrito vaciado')),
        );
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error vaciando carrito: $e')),
        );
      }
    }
  }

  void _proceedToCheckout() {
    if (_cartItems.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('El carrito está vacío')),
      );
      return;
    }
    Navigator.pushNamed(context, '/checkout');
  }

  void _continueShopping() {
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Carrito de Compras'),
        actions: [
          CartIcon(),
        ],
      ),
      body: _loading
          ? Center(child: CircularProgressIndicator())
          : _error.isNotEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.error, size: 64, color: Colors.red),
                      SizedBox(height: 16),
                      Text('Error: $_error'),
                      SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _loadCart,
                        child: Text('Reintentar'),
                      ),
                    ],
                  ),
                )
              : _cartItems.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.shopping_cart_outlined, size: 64, color: Colors.grey),
                          SizedBox(height: 16),
                          Text(
                            'Tu carrito está vacío',
                            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                          ),
                          SizedBox(height: 8),
                          Text(
                            'Agrega algunos productos increíbles',
                            style: TextStyle(color: Colors.grey),
                          ),
                          SizedBox(height: 24),
                          ElevatedButton(
                            onPressed: _continueShopping,
                            child: Text('Seguir Comprando'),
                          ),
                        ],
                      ),
                    )
                  : Column(
                      children: [
                        Expanded(
                          child: ListView.builder(
                            itemCount: _cartItems.length,
                            itemBuilder: (context, index) {
                              final item = _cartItems[index];
                              return Dismissible(
                                key: Key(item.id.toString()),
                                background: Container(color: Colors.red),
                                onDismissed: (direction) => _removeItem(item.id),
                                child: Card(
                                  margin: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                  child: ListTile(
                                    leading: item.productoImagen != null
                                        ? Image.network(item.productoImagen!)
                                        : Icon(Icons.shopping_bag, size: 40),
                                    title: Text(
                                      item.productoNombre,
                                      style: TextStyle(fontWeight: FontWeight.bold),
                                    ),
                                    subtitle: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Text('\$${item.productoPrecio} c/u'),
                                        Text('Stock: ${item.productoStock}'),
                                      ],
                                    ),
                                    trailing: Row(
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        IconButton(
                                          icon: Icon(Icons.remove),
                                          onPressed: () => _updateQuantity(item, item.cantidad - 1),
                                        ),
                                        Text('${item.cantidad}'),
                                        IconButton(
                                          icon: Icon(Icons.add),
                                          onPressed: () => _updateQuantity(item, item.cantidad + 1),
                                        ),
                                        SizedBox(width: 16),
                                        Text(
                                          '\$${item.subtotal.toStringAsFixed(2)}',
                                          style: TextStyle(
                                            fontWeight: FontWeight.bold,
                                            color: Colors.green,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              );
                            },
                          ),
                        ),
                        Container(
                          padding: EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            boxShadow: [
                              BoxShadow(
                                offset: Offset(0, -2),
                                blurRadius: 4,
                                color: Colors.black12,
                              ),
                            ],
                          ),
                          child: Column(
                            children: [
                              Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Text(
                                    'Total:',
                                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                                  ),
                                  Text(
                                    '\$$_totalPrice',
                                    style: TextStyle(
                                      fontSize: 18,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.green,
                                    ),
                                  ),
                                ],
                              ),
                              SizedBox(height: 16),
                              Row(
                                children: [
                                  Expanded(
                                    child: OutlinedButton(
                                      onPressed: _clearCart,
                                      style: OutlinedButton.styleFrom(
                                        foregroundColor: Colors.red,
                                        side: BorderSide(color: Colors.red),
                                      ),
                                      child: Text('Vaciar Carrito'),
                                    ),
                                  ),
                                  SizedBox(width: 16),
                                  Expanded(
                                    child: ElevatedButton(
                                      onPressed: _proceedToCheckout,
                                      style: ElevatedButton.styleFrom(
                                        backgroundColor: Colors.green,
                                      ),
                                      child: Text('Pagar'),
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
    );
  }
}