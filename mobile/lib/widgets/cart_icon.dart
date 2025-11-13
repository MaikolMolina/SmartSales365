import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/cart_service.dart';

class CartIcon extends StatefulWidget {
  final VoidCallback? onPressed;

  const CartIcon({Key? key, this.onPressed}) : super(key: key);

  @override
  _CartIconState createState() => _CartIconState();
}

class _CartIconState extends State<CartIcon> {
  int _itemCount = 0;

  @override
  void initState() {
    super.initState();
    _loadCartCount();
  }

  Future<void> _loadCartCount() async {
    try {
      final summary = await CartService().getCartSummary();
      if (mounted) {
        setState(() {
          _itemCount = summary.totalItems;
        });
      }
    } catch (e) {
      // Silently fail, cart might be empty
      if (mounted) {
        setState(() {
          _itemCount = 0;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        IconButton(
          icon: Icon(Icons.shopping_cart),
          onPressed: widget.onPressed ?? () {
            Navigator.pushNamed(context, '/cart');
          },
        ),
        if (_itemCount > 0)
          Positioned(
            right: 8,
            top: 8,
            child: Container(
              padding: EdgeInsets.all(2),
              decoration: BoxDecoration(
                color: Colors.red,
                borderRadius: BorderRadius.circular(6),
              ),
              constraints: BoxConstraints(
                minWidth: 14,
                minHeight: 14,
              ),
              child: Text(
                '$_itemCount',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 8,
                ),
                textAlign: TextAlign.center,
              ),
            ),
          ),
      ],
    );
  }
}