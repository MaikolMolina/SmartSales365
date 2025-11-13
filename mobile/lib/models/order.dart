class Order {
  final int id;
  final List<dynamic> items;
  final double total;
  final String estado;
  final DateTime fechaCreacion;
  final DateTime? fechaCompletada;
  final Map<String, dynamic>? direccionEnvio;

  Order({
    required this.id,
    required this.items,
    required this.total,
    required this.estado,
    required this.fechaCreacion,
    this.fechaCompletada,
    this.direccionEnvio,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      id: json['id'],
      items: json['items'],
      total: double.parse(json['total'].toString()),
      estado: json['estado'],
      fechaCreacion: DateTime.parse(json['fecha_creacion']),
      fechaCompletada: json['fecha_completada'] != null 
          ? DateTime.parse(json['fecha_completada'])
          : null,
      direccionEnvio: json['direccion_envio'],
    );
  }

  String get formattedDate {
    return '${fechaCreacion.day}/${fechaCreacion.month}/${fechaCreacion.year}';
  }

  String get statusText {
    switch (estado) {
      case 'PENDIENTE':
        return 'Pendiente';
      case 'PROCESANDO':
        return 'Procesando';
      case 'COMPLETADA':
        return 'Completada';
      case 'CANCELADA':
        return 'Cancelada';
      default:
        return estado;
    }
  }
}