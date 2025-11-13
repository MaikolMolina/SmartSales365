class PaymentIntent {
  final String sessionId;
  final String urlPago;
  final int pagoId;
  final int ordenId;
  final double total;

  PaymentIntent({
    required this.sessionId,
    required this.urlPago,
    required this.pagoId,
    required this.ordenId,
    required this.total,
  });

  factory PaymentIntent.fromJson(Map<String, dynamic> json) {
    return PaymentIntent(
      sessionId: json['session_id'],
      urlPago: json['url_pago'],
      pagoId: json['pago_id'],
      ordenId: json['orden_id'],
      total: double.parse(json['total'].toString()),
    );
  }
}

class PaymentResult {
  final bool success;
  final String message;
  final List<dynamic>? ventasCreadas;
  final double? totalCompra;
  final int? numeroVentas;

  PaymentResult({
    required this.success,
    required this.message,
    this.ventasCreadas,
    this.totalCompra,
    this.numeroVentas,
  });

  factory PaymentResult.fromJson(Map<String, dynamic> json) {
    return PaymentResult(
      success: json['message'] != null,
      message: json['message'] ?? 'Error en el pago',
      ventasCreadas: json['ventas_creadas'],
      totalCompra: json['total_compra'] != null 
          ? double.parse(json['total_compra'].toString())
          : null,
      numeroVentas: json['numero_ventas'],
    );
  }
}