import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../../models/payment_intent.dart';
import 'payment_success_screen.dart';

class PaymentScreen extends StatefulWidget {
  final PaymentIntent paymentIntent;

  const PaymentScreen({Key? key, required this.paymentIntent}) : super(key: key);

  @override
  State<PaymentScreen> createState() => _PaymentScreenState();
}

class _PaymentScreenState extends State<PaymentScreen> {
  late final WebViewController _controller;
  bool _loading = true;
  bool _paymentCompleted = false;

  @override
  void initState() {
    super.initState();

    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageStarted: (String url) {
            setState(() => _loading = true);
          },
          onPageFinished: (String url) {
            setState(() => _loading = false);
            if (url.contains('payment-success') || url.contains('success')) {
              _paymentCompleted = true;
              _navigateToSuccessScreen();
            }
          },
          onNavigationRequest: (NavigationRequest request) {
            if (request.url.contains('payment-success') || request.url.contains('success')) {
              _paymentCompleted = true;
              WidgetsBinding.instance.addPostFrameCallback((_) {
                _navigateToSuccessScreen();
              });
              return NavigationDecision.prevent;
            }
            return NavigationDecision.navigate;
          },
        ),
      )
      ..loadRequest(Uri.parse(widget.paymentIntent.urlPago));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Procesando Pago'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            if (_paymentCompleted) {
              Navigator.pushReplacementNamed(context, '/payment-success');
            } else {
              Navigator.pop(context);
            }
          },
        ),
      ),
      body: Stack(
        children: [
          WebViewWidget(controller: _controller),
          if (_loading)
            const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Cargando pasarela de pago...'),
                ],
              ),
            ),
        ],
      ),
    );
  }

  void _navigateToSuccessScreen() {
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (context) => PaymentSuccessScreen(
          sessionId: widget.paymentIntent.sessionId,
          orderId: widget.paymentIntent.ordenId,
        ),
      ),
    );
  }
}
