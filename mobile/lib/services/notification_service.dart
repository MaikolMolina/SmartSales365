import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'api.dart';

class NotificationService {
  static final NotificationService _instance = NotificationService._internal();
  factory NotificationService() => _instance;
  NotificationService._internal();

  final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;
  late FlutterLocalNotificationsPlugin _flutterLocalNotificationsPlugin;

  // Canal para notificaciones
  static const AndroidNotificationChannel _channel = AndroidNotificationChannel(
    'smart_sales_365_channel', // id
    'SmartSales365 Notifications', // title
    description: 'Canal para notificaciones importantes de SmartSales365',
    importance: Importance.high,
    playSound: true,
    enableVibration: true,
  );

  Future<void> initialize() async {
    try {
      // Inicializar Firebase
      await Firebase.initializeApp();
      
      // Configurar Local Notifications
      _flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();
      
      const AndroidInitializationSettings initializationSettingsAndroid =
          AndroidInitializationSettings('@mipmap/ic_launcher');
      
      final InitializationSettings initializationSettings =
          InitializationSettings(android: initializationSettingsAndroid);
      
      await _flutterLocalNotificationsPlugin.initialize(
        initializationSettings,
        onDidReceiveNotificationResponse: (NotificationResponse details) {
          // Manejar cuando se presiona la notificación
          _onNotificationTap(details.payload);
        },
      );

      // Crear canal de notificaciones
      await _flutterLocalNotificationsPlugin
          .resolvePlatformSpecificImplementation<
              AndroidFlutterLocalNotificationsPlugin>()
          ?.createNotificationChannel(_channel);

      // Solicitar permisos
      await _requestPermissions();

      // Configurar manejadores de mensajes
      _setupMessageHandlers();

      // Obtener y guardar token
      await _setupFcmToken();

      print('✅ Servicio de notificaciones inicializado correctamente');

    } catch (e) {
      print('❌ Error inicializando notificaciones: $e');
    }
  }

  Future<void> _requestPermissions() async {
    NotificationSettings settings = await _firebaseMessaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
      carPlay: false,
      criticalAlert: false,
      provisional: false,
    );

    print('Estado de permisos: ${settings.authorizationStatus}');
  }

  void _setupMessageHandlers() {
    // Mensaje en primer plano
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      print('📱 Mensaje en primer plano recibido');
      _showNotification(message);
    });

    // Cuando se presiona la notificación y la app está en segundo plano/terminada
    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
      print('🔔 Notificación presionada (app en background)');
      _handleNotificationClick(message);
    });

    // Mensaje en background (manejado automáticamente por el servicio nativo)
  }

  Future<void> _setupFcmToken() async {
    try {
      // Obtener token
      String? token = await _firebaseMessaging.getToken();
      
      if (token != null) {
        print('🔑 FCM Token: $token');
        
        // Guardar token localmente
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('fcm_token', token);
        
        // Enviar token al backend
        await _sendTokenToServer(token);
      }

      // Escuchar cambios en el token
      _firebaseMessaging.onTokenRefresh.listen((newToken) async {
        print('🔄 Token actualizado: $newToken');
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('fcm_token', newToken);
        await _sendTokenToServer(newToken);
      });

    } catch (e) {
      print('❌ Error obteniendo FCM token: $e');
    }
  }

  Future<void> _sendTokenToServer(String token) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final authToken = prefs.getString('token') ?? '';
  
      final response = await ApiService.post(
        '/auth/save_fcm_token/',
        {'fcm_token': token},
        headers: {
          'Authorization': 'Token $authToken',
        },
      );
  
      if (response.statusCode == 200) {
        print('✅ Token enviado al servidor exitosamente');
      } else {
        print('❌ Error enviando token: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      print('❌ Error enviando token: $e');
    }
  }

  Future<void> _showNotification(RemoteMessage message) async {
    try {
      final notification = message.notification;
      final android = message.notification?.android;

      if (notification != null) {
        AndroidNotificationDetails androidPlatformChannelSpecifics =
            AndroidNotificationDetails(
          _channel.id,
          _channel.name,
          channelDescription: _channel.description,
          importance: Importance.high,
          priority: Priority.high,
          playSound: true,
          enableVibration: true,
          //sound: const RawResourceAndroidNotificationSound('notification'),
          styleInformation: const BigTextStyleInformation(''),
        );

        NotificationDetails platformChannelSpecifics =
            NotificationDetails(android: androidPlatformChannelSpecifics);

        await _flutterLocalNotificationsPlugin.show(
          DateTime.now().millisecondsSinceEpoch.remainder(100000),
          notification.title ?? 'SmartSales365',
          notification.body ?? 'Nueva notificación',
          platformChannelSpecifics,
          payload: message.data['type'] ?? 'general',
        );
      }
    } catch (e) {
      print('❌ Error mostrando notificación: $e');
    }
  }

  void _handleNotificationClick(RemoteMessage message) {
    // Aquí puedes manejar la navegación cuando se presiona la notificación
    final data = message.data;
    final type = data['type'] ?? 'general';
    
    print('🔔 Notificación clickeada - Tipo: $type');
    
    // Ejemplo: Navegar a diferentes pantallas según el tipo de notificación
    switch (type) {
      case 'sale':
        // Navigator.push(context, MaterialPageRoute(builder: (_) => SalesScreen()));
        break;
      case 'promotion':
        // Navigator.push(context, MaterialPageRoute(builder: (_) => PromotionsScreen()));
        break;
      default:
        // Navigator.push(context, MaterialPageRoute(builder: (_) => NotificationsScreen()));
        break;
    }
  }

  void _onNotificationTap(String? payload) {
    // Manejar tap en notificación cuando la app está en primer plano
    print('🔔 Notificación presionada (primer plano) - Payload: $payload');
  }

  // Método para suscribirse a temas
  Future<void> subscribeToTopic(String topic) async {
    try {
      await _firebaseMessaging.subscribeToTopic(topic);
      print('✅ Suscrito al tema: $topic');
    } catch (e) {
      print('❌ Error suscribiéndose al tema $topic: $e');
    }
  }

  // Método para cancelar suscripción
  Future<void> unsubscribeFromTopic(String topic) async {
    try {
      await _firebaseMessaging.unsubscribeFromTopic(topic);
      print('✅ Cancelada suscripción al tema: $topic');
    } catch (e) {
      print('❌ Error cancelando suscripción al tema $topic: $e');
    }
  }

  // Obtener token actual
  Future<String?> getCurrentToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('fcm_token');
  }
}