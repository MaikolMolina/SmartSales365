import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../../services/payment_service.dart';
import '../payments/payment_success_screen.dart';
import '../payments/payment_screen.dart';

class CheckoutScreen extends StatefulWidget {
  @override
  _CheckoutScreenState createState() => _CheckoutScreenState();
}

class _CheckoutScreenState extends State<CheckoutScreen> {
  bool _processing = false;

  Future<void> _processPayment() async {
    setState(() {
      _processing = true;
    });

    try {
      final paymentIntent = await PaymentService().createPaymentFromCart();
      
      // Navegar a la pantalla de pago con WebView
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => PaymentScreen(paymentIntent: paymentIntent),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error procesando el pago: $e')),
      );
    } finally {
      if (mounted) {
        setState(() {
          _processing = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Checkout'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Card(
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Resumen del Pedido',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    SizedBox(height: 16),
                    ListTile(
                      leading: Icon(Icons.payment, color: Colors.blue),
                      title: Text('Método de Pago'),
                      subtitle: Text('Stripe - Tarjeta de Crédito/Débito'),
                    ),
                    ListTile(
                      leading: Icon(Icons.security, color: Colors.green),
                      title: Text('Pago Seguro'),
                      subtitle: Text('Tus datos están protegidos con encriptación SSL'),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(height: 16),
            Card(
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Información Importante',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    SizedBox(height: 8),
                    Text('• Serás redirigido a Stripe para completar el pago'),
                    Text('• Tu pedido se procesará automáticamente después del pago'),
                    Text('• Recibirás una confirmación por email'),
                  ],
                ),
              ),
            ),
            Spacer(),
            ElevatedButton(
              onPressed: _processing ? null : _processPayment,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green,
                padding: EdgeInsets.symmetric(vertical: 16),
              ),
              child: _processing
                  ? Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        CircularProgressIndicator(color: Colors.white),
                        SizedBox(width: 8),
                        Text('Procesando...'),
                      ],
                    )
                  : Text(
                      'Continuar con el Pago',
                      style: TextStyle(fontSize: 16),
                    ),
            ),
            SizedBox(height: 8),
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('Cancelar'),
            ),
          ],
        ),
      ),
    );
  }
}