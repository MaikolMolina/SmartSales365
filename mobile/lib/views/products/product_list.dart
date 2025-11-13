import 'package:flutter/material.dart';
import '../../services/cart_service.dart';
import '../../services/api.dart';
import 'dart:convert';

class ProductList extends StatefulWidget {
  @override
  _ProductListState createState() => _ProductListState();
}

class _ProductListState extends State<ProductList> {
  List<dynamic> _products = [];
  bool _loading = true;
  String _error = '';
  String _search = '';
  String _categoryFilter = '';

  @override
  void initState() {
    super.initState();
    _loadProducts();
  }

  Future<void> _loadProducts() async {
    try {
      final response = await ApiService.get('/commercial/productos/');
      if (response.statusCode == 200) {
        setState(() {
          _products = jsonDecode(response.body);
          _loading = false;
        });
      } else {
        throw Exception('Error cargando productos');
      }
    } catch (e) {
      setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }

  Future<void> _addToCart(int productId, String name) async {
    try {
      await CartService().addToCart(productId, 1);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('$name agregado al carrito'),
          action: SnackBarAction(
            label: 'Ver Carrito',
            onPressed: () {
              Navigator.pushNamed(context, '/cart');
            },
          ),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error agregando al carrito: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return Center(child: CircularProgressIndicator());
    if (_error.isNotEmpty) return Center(child: Text('Error: $_error'));

    final categories = _products.map((p) => p['categoria_nombre']).toSet().toList();
    final filtered = _products.where((p) {
      final matchSearch = p['nombre'].toString().toLowerCase().contains(_search.toLowerCase());
      final matchCategory = _categoryFilter.isEmpty || p['categoria_nombre'] == _categoryFilter;
      return matchSearch && matchCategory;
    }).toList();

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8),
          child: Row(
            children: [
              Expanded(
                child: TextField(
                  decoration: InputDecoration(labelText: 'Buscar productos'),
                  onChanged: (v) => setState(() => _search = v),
                ),
              ),
              SizedBox(width: 8),
              DropdownButton<String>(
                value: _categoryFilter.isEmpty ? null : _categoryFilter,
                hint: Text('Categoría'),
                items: categories.map((c) => DropdownMenuItem<String>(
                  value: c.toString(),
                  child: Text(c.toString()),
                )).toList(),
                onChanged: (val) => setState(() => _categoryFilter = val ?? ''),
              ),    
            ],
          ),
        ),
        Expanded(
          child: ListView.builder(
            itemCount: filtered.length,
            itemBuilder: (context, index) {
              final p = filtered[index];
              return Card(
                margin: EdgeInsets.symmetric(vertical: 4, horizontal: 8),
                child: ListTile(
                  title: Text(p['nombre']),
                  subtitle: Text(p['categoria_nombre']),
                  trailing: ElevatedButton(
                    onPressed: p['stock'] > 0 ? () => _addToCart(p['id'], p['nombre']) : null,
                    child: Text(p['stock'] > 0 ? 'Agregar' : 'Agotado'),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
