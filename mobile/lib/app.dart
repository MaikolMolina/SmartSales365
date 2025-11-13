import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'services/auth_service.dart';
import 'services/notification_service.dart';
import 'views/auth/login_screen.dart';
import 'views/auth/home_screen.dart';
import 'views/notifications/notifications_screen.dart';

// 🔹 Importa las nuevas vistas
import 'views/client/client_home.dart';
import 'views/products/product_list.dart';
import 'views/cart/cart_screen.dart';
import 'views/cart/checkout_screen.dart';
import 'views/payments/payment_success_screen.dart';

class App extends StatefulWidget {
  const App({Key? key}) : super(key: key);

  @override
  _AppState createState() => _AppState();
}

class _AppState extends State<App> {
  final AuthService _authService = AuthService();
  final NotificationService _notificationService = NotificationService();

  @override
  void initState() {
    super.initState();
    _initializeApp();
  }

  Future<void> _initializeApp() async {
    // Inicializar servicios
    await _notificationService.initialize();
  }

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        Provider<AuthService>.value(value: _authService),
      ],
      child: MaterialApp(
        title: 'SmartSales365',
        theme: ThemeData(
          primarySwatch: Colors.blue,
          useMaterial3: true,
        ),
        routes: {
          // 🔹 Rutas existentes
          '/login': (context) => LoginScreen(),
          '/home': (context) => HomeScreen(),
          '/notifications': (context) => NotificationsScreen(),

          // 🔹 Nuevas rutas agregadas
          '/client-home': (context) => ClientHome(),
          '/products': (context) => ProductList(),
          '/cart': (context) => CartScreen(),
          '/checkout': (context) => CheckoutScreen(),
          '/payment-success': (context) => PaymentSuccessScreen(
                sessionId: '',
                orderId: 0,
              ),
        },
        home: FutureBuilder<bool>(
          future: _authService.isLoggedIn(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Scaffold(
                body: Center(child: CircularProgressIndicator()),
              );
            } else {
              if (snapshot.hasData && snapshot.data!) {
                // 🔹 Al iniciar sesión, se redirige a ClientHome (como en la nueva versión)
                return ClientHome();
              } else {
                return LoginScreen();
              }
            }
          },
        ),
      ),
    );
  }
}
