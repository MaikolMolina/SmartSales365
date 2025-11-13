import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/cart_item.dart';
import '../models/payment_intent.dart';
import 'api.dart';

class CartService {
  static final CartService _instance = CartService._internal();
  factory CartService() => _instance;
  CartService._internal();

  Future<CartResponse> getCart() async {
    final response = await ApiService.get('/commercial/carrito/mi_carrito/');
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return CartResponse.fromJson(data);
    } else {
      throw Exception('Error al cargar el carrito: ${response.statusCode}');
    }
  }

  Future<CartItem> addToCart(int productId, int quantity) async {
    final response = await ApiService.post('/commercial/carrito/agregar_producto/', {
      'producto_id': productId,
      'cantidad': quantity,
    });

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return CartItem.fromJson(data['item']);
    } else {
      final errorData = jsonDecode(response.body);
      throw Exception(errorData['error'] ?? 'Error al agregar al carrito');
    }
  }

  Future<CartItem> updateCartItem(int itemId, int quantity) async {
    final response = await ApiService.post(
      '/commercial/carrito/$itemId/actualizar_cantidad/',
      {'cantidad': quantity}
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return CartItem.fromJson(data['item']);
    } else {
      final errorData = jsonDecode(response.body);
      throw Exception(errorData['error'] ?? 'Error actualizando cantidad');
    }
  }

  Future<void> removeFromCart(int itemId) async {
    final response = await ApiService.delete('/commercial/carrito/$itemId/');

    if (response.statusCode != 200 && response.statusCode != 204) {
      throw Exception('Error eliminando producto del carrito');
    }
  }

  Future<void> clearCart() async {
    final response = await ApiService.post('/commercial/carrito/vaciar_carrito/', {});

    if (response.statusCode != 200) {
      throw Exception('Error vaciando el carrito');
    }
  }

  Future<CartSummary> getCartSummary() async {
    final response = await ApiService.get('/commercial/carrito/resumen/');

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return CartSummary.fromJson(data);
    } else {
      throw Exception('Error cargando resumen del carrito');
    }
  }

  Future<PaymentResult> checkout() async {
    final response = await ApiService.post('/commercial/carrito/finalizar_compra/', {});

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return PaymentResult.fromJson(data);
    } else {
      final errorData = jsonDecode(response.body);
      throw Exception(errorData['error'] ?? 'Error finalizando compra');
    }
  }
}