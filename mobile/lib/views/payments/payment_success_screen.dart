import 'package:flutter/material.dart';

class PaymentSuccessScreen extends StatelessWidget {
  final String sessionId;
  final int orderId;

  const PaymentSuccessScreen({
    Key? key,
    required this.sessionId,
    required this.orderId,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.check_circle,
                color: Colors.green,
                size: 80,
              ),
              SizedBox(height: 24),
              Text(
                '¡Pago Exitoso!',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Colors.green,
                ),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 16),
              Text(
                'Gracias por tu compra. Tu pedido ha sido procesado correctamente.',
                style: TextStyle(fontSize: 16),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 24),
              Card(
                child: Padding(
                  padding: EdgeInsets.all(16),
                  child: Column(
                    children: [
                      ListTile(
                        leading: Icon(Icons.receipt),
                        title: Text('Número de Orden'),
                        subtitle: Text('#$orderId'),
                      ),
                      ListTile(
                        leading: Icon(Icons.credit_card),
                        title: Text('ID de Transacción'),
                        subtitle: Text(
                          sessionId,
                          style: TextStyle(fontSize: 12),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              SizedBox(height: 32),
              Column(
                children: [
                  ElevatedButton(
                    onPressed: () {
                      Navigator.pushNamedAndRemoveUntil(
                        context,
                        '/client-home',
                        (route) => false,
                      );
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      padding: EdgeInsets.symmetric(horizontal: 32, vertical: 12),
                    ),
                    child: Text('Volver al Inicio'),
                  ),
                  SizedBox(height: 12),
                  TextButton(
                    onPressed: () {
                      Navigator.pushNamed(context, '/my-orders');
                    },
                    child: Text('Ver Mis Pedidos'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}