import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'http://10.0.2.2:8000/api'; // Android emulator

  // -----------------------
  // GET
  // -----------------------
  static Future<http.Response> get(String endpoint, {Map<String, String>? headers}) async {
    final prefs = await SharedPreferences.getInstance();
    final sessionCookie = prefs.getString('session_cookie');

    final finalHeaders = {
      'Content-Type': 'application/json',
      if (sessionCookie != null) 'Cookie': sessionCookie,
      if (headers != null) ...headers,
    };

    return await http.get(Uri.parse('$baseUrl$endpoint'), headers: finalHeaders);
  }

  // -----------------------
  // POST
  // -----------------------
  static Future<http.Response> post(String endpoint, dynamic data, {Map<String, String>? headers}) async {
    final prefs = await SharedPreferences.getInstance();
    final sessionCookie = prefs.getString('session_cookie');

    final finalHeaders = {
      'Content-Type': 'application/json',
      if (sessionCookie != null) 'Cookie': sessionCookie,
      if (headers != null) ...headers,
    };

    final response = await http.post(
      Uri.parse('$baseUrl$endpoint'),
      headers: finalHeaders,
      body: jsonEncode(data),
    );

    // Guardar cookie si viene
    if (response.headers['set-cookie'] != null) {
      await prefs.setString('session_cookie', response.headers['set-cookie']!);
    }

    return response;
  }

  // -----------------------
  // PUT
  // -----------------------
  static Future<http.Response> put(String endpoint, dynamic data, {Map<String, String>? headers}) async {
    final prefs = await SharedPreferences.getInstance();
    final sessionCookie = prefs.getString('session_cookie');

    final finalHeaders = {
      'Content-Type': 'application/json',
      if (sessionCookie != null) 'Cookie': sessionCookie,
      if (headers != null) ...headers,
    };

    final response = await http.put(
      Uri.parse('$baseUrl$endpoint'),
      headers: finalHeaders,
      body: jsonEncode(data),
    );

    if (response.headers['set-cookie'] != null) {
      await prefs.setString('session_cookie', response.headers['set-cookie']!);
    }

    return response;
  }

  // -----------------------
  // DELETE
  // -----------------------
  static Future<http.Response> delete(String endpoint, {Map<String, String>? headers}) async {
    final prefs = await SharedPreferences.getInstance();
    final sessionCookie = prefs.getString('session_cookie');

    final finalHeaders = {
      'Content-Type': 'application/json',
      if (sessionCookie != null) 'Cookie': sessionCookie,
      if (headers != null) ...headers,
    };

    return await http.delete(Uri.parse('$baseUrl$endpoint'), headers: finalHeaders);
  }

  // -----------------------
  // POST Multipart
  // -----------------------
  static Future<http.StreamedResponse> postMultipart(String endpoint, http.MultipartRequest request) async {
    final prefs = await SharedPreferences.getInstance();
    final sessionCookie = prefs.getString('session_cookie');

    request.headers['Cookie'] = sessionCookie ?? '';
    request.headers['Content-Type'] = 'multipart/form-data';

    return await request.send();
  }
}
