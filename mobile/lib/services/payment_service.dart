import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/payment_intent.dart';
import '../models/order.dart';
import 'api.dart';

class PaymentService {
  static final PaymentService _instance = PaymentService._internal();
  factory PaymentService() => _instance;
  PaymentService._internal();

  Future<PaymentIntent> createPaymentFromCart() async {
    final response = await ApiService.post('/commercial/pagos/pago_desde_carrito/', {});

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return PaymentIntent.fromJson(data);
    } else {
      final errorData = jsonDecode(response.body);
      throw Exception(errorData['error'] ?? 'Error creando pago desde carrito');
    }
  }

  Future<PaymentIntent> createPaymentSession(int? orderId, double? amount, String? description) async {
    final Map<String, dynamic> data = {};
    
    if (orderId != null) {
      data['orden_id'] = orderId;
    } else {
      data['monto'] = amount;
      data['descripcion'] = description;
    }

    final response = await ApiService.post('/commercial/pagos/crear_sesion_pago/', data);

    if (response.statusCode == 200) {
      final result = jsonDecode(response.body);
      return PaymentIntent.fromJson(result);
    } else {
      final errorData = jsonDecode(response.body);
      throw Exception(errorData['error'] ?? 'Error creando sesión de pago');
    }
  }

  Future<Map<String, dynamic>> verifyPaymentStatus(int paymentId) async {
    final response = await ApiService.get('/commercial/pagos/$paymentId/verificar_estado/');

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Error verificando estado del pago');
    }
  }

  Future<List<Order>> getMyOrders() async {
    final response = await ApiService.get('/commercial/ordenes/');

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final List<dynamic> results = data['results'] ?? data;
      return results.map((order) => Order.fromJson(order)).toList();
    } else {
      throw Exception('Error cargando órdenes');
    }
  }

  Future<Order> getOrder(int orderId) async {
    final response = await ApiService.get('/commercial/ordenes/$orderId/');

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return Order.fromJson(data);
    } else {
      throw Exception('Error cargando orden');
    }
  }
}