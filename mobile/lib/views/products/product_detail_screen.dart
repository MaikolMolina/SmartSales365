// Agregar esta función al ProductList
void _addToCart(Product product) async {
  try {
    await CartService().addToCart(product.id, 1);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('${product.nombre} agregado al carrito'),
        action: SnackBarAction(
          label: 'Ver Carrito',
          onPressed: () {
            Navigator.pushNamed(context, '/cart');
          },
        ),
      ),
    );
  } catch (e) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Error: $e')),
    );
  }
}

// En el ProductCard, agregar el botón de agregar al carrito:
ListTile(
  // ... contenido existente ...
  trailing: IconButton(
    icon: Icon(Icons.add_shopping_cart),
    onPressed: () => _addToCart(product),
  ),
)