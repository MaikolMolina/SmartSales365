class CartItem {
  final int id;
  final int productoId;
  final String productoNombre;
  final double productoPrecio;
  final int productoStock;
  final String? productoImagen;
  int cantidad;

  CartItem({
    required this.id,
    required this.productoId,
    required this.productoNombre,
    required this.productoPrecio,
    required this.productoStock,
    this.productoImagen,
    required this.cantidad,
  });

  factory CartItem.fromJson(Map<String, dynamic> json) {
    return CartItem(
      id: json['id'],
      productoId: json['producto'],
      productoNombre: json['producto_nombre'],
      productoPrecio: double.parse(json['producto_precio'].toString()),
      productoStock: json['producto_stock'],
      productoImagen: json['producto_imagen'],
      cantidad: json['cantidad'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'producto': productoId,
      'producto_nombre': productoNombre,
      'producto_precio': productoPrecio,
      'producto_stock': productoStock,
      'producto_imagen': productoImagen,
      'cantidad': cantidad,
    };
  }

  double get subtotal => productoPrecio * cantidad;

  CartItem copyWith({
    int? cantidad,
  }) {
    return CartItem(
      id: id,
      productoId: productoId,
      productoNombre: productoNombre,
      productoPrecio: productoPrecio,
      productoStock: productoStock,
      productoImagen: productoImagen,
      cantidad: cantidad ?? this.cantidad,
    );
  }
}

class CartSummary {
  final int totalItems;
  final int totalCantidad;
  final double totalPrecio;

  CartSummary({
    required this.totalItems,
    required this.totalCantidad,
    required this.totalPrecio,
  });

  factory CartSummary.fromJson(Map<String, dynamic> json) {
    return CartSummary(
      totalItems: json['total_items'],
      totalCantidad: json['total_cantidad'],
      totalPrecio: double.parse(json['total_precio'].toString()),
    );
  }
}

class CartResponse {
  final List<CartItem> items;
  final CartSummary resumen;

  CartResponse({
    required this.items,
    required this.resumen,
  });

  factory CartResponse.fromJson(Map<String, dynamic> json) {
    final items = (json['items'] as List)
        .map((item) => CartItem.fromJson(item))
        .toList();
    
    final resumen = CartSummary.fromJson(json['resumen']);
    
    return CartResponse(
      items: items,
      resumen: resumen,
    );
  }
}