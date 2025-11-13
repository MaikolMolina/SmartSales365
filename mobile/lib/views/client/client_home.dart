import 'package:flutter/material.dart';
import '../../widgets/cart_icon.dart';
import '../../services/auth_service.dart';
import '../products/product_list.dart';
import '../auth/login_screen.dart';

class ClientHome extends StatefulWidget {
  @override
  _ClientHomeState createState() => _ClientHomeState();
}

class _ClientHomeState extends State<ClientHome> {
  final AuthService _auth = AuthService();

  void _logout() {
    _auth.logout();
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => LoginScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    final user = _auth.user;
    return Scaffold(
      appBar: AppBar(
        title: Text('Inicio Cliente'),
        actions: [
          CartIcon(),
          IconButton(
            icon: Icon(Icons.logout),
            onPressed: _logout,
            tooltip: 'Cerrar sesión',
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Bienvenido, ${user?.firstName ?? ''} ${user?.lastName ?? ''}',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                SizedBox(height: 8),
                Text('Explora nuestros productos y encuentra lo que necesitas'),
              ],
            ),
          ),
          Expanded(child: ProductList()),
        ],
      ),
    );
  }
}
