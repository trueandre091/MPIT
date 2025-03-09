import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';

class AuthService {
  static const String baseUrl = 'http://10.0.2.2:8000/api/auth';
  static const String tokenKey = 'auth_token';
  final SharedPreferences _prefs;

  AuthService(this._prefs);

  static Future<AuthService> create() async {
    final prefs = await SharedPreferences.getInstance();
    return AuthService(prefs);
  }

  Future<bool> isAuthenticated() async {
    try {
      if (_prefs.containsKey(tokenKey)) {
        if (await isVerified()) {
          return true;
        } else {
          return false;
        }
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  Future<bool> tokenExists() async {
    return _prefs.containsKey(tokenKey);
  }

  Future<bool> isVerified() async {
    final response = await me();
    return response['status'] == 200;
  }

  Future<void> saveToken(String token) async {
    await _prefs.setString(tokenKey, token);
  }

  Future<void> clearToken() async {
    await _prefs.remove(tokenKey);
  }

  String? getToken() {
    return _prefs.getString(tokenKey);
  }

  Future<Map<String, dynamic>> me() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/me'),
        headers: {
          'Authorization': 'Bearer ${getToken()}',
        },
      ).timeout(Duration(seconds: 3));

      if (response.statusCode == 200) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        return {'user': User.fromJson(data['user']), 'status': 200, 'detail': null};
      } else if (response.statusCode == 401) {
        clearToken();
        return {'user': null, 'status': 401, 'detail': json.decode(response.body)['detail']};
      } else {
        return {'user': null, 'status': response.statusCode, 'detail': json.decode(response.body)['detail']};
      }
    } catch (e) {
      return {'user': null, 'status': 404, 'detail': 'Timeout error'};
    }
  }

  Future<Map<String, dynamic>> login(String email, String password) async {
    Map<String, String> formData = {
      'email': email,
      'password': password,
    };
    final response = await http.post(
      Uri.parse('$baseUrl/login'),
      headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
      body: formData,
    );

    if (response.statusCode == 200) {
      final data = json.decode(utf8.decode(response.bodyBytes));
      final token = data['token'];
      await saveToken(token);
      return {'user': User.fromJson(data['user']), 'status': 200, 'detail': null};
    } else if (response.statusCode == 403) {
      return {'user': null, 'status': 403, 'detail': json.decode(utf8.decode(response.bodyBytes))['detail']};
    } else if (response.statusCode == 404) {
      return {'user': null, 'status': 404, 'detail': json.decode(utf8.decode(response.bodyBytes))['detail']};
    } else {
      return {'user': null, 'status': response.statusCode, 'detail': json.decode(response.body)['detail']};
    }
  }

  Future<Map<String, dynamic>> register(String email, String password, String name) async {
    Map<String, String> formData = {
      'email': email,
      'password': password,
      'name': name,
    };

    final response = await http.post(
      Uri.parse('$baseUrl/register'),
      headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
      body: formData,
    );

    if (response.statusCode == 201) {
      final data = json.decode(utf8.decode(response.bodyBytes));
      final token = data['token'];
      await saveToken(token);
      return {'user': User.fromJson(data['user']), 'status': 201, 'detail': null};
    } else if (response.statusCode == 406) {
      return {'user': null, 'status': 406, 'detail': json.decode(utf8.decode(response.bodyBytes))['detail']};
    } else {
      return {'user': null, 'status': response.statusCode, 'detail': json.decode(response.body)['detail']};
    }
  }

  Future<Map<String, dynamic>> logout() async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/logout'),
        headers: {
          'Authorization': 'Bearer ${getToken()}',
        },
      ).timeout(Duration(seconds: 3));

      if (response.statusCode == 200) {
        await clearToken();
        return {'status': 200, 'detail': null};
      } else if (response.statusCode == 401) {
        return {'status': 401, 'detail': json.decode(utf8.decode(response.bodyBytes))['detail']};
      } else if (response.statusCode == 403) {
        return {'status': 403, 'detail': json.decode(utf8.decode(response.bodyBytes))['detail']};
      } else if (response.statusCode == 404) {
        return {'status': 404, 'detail': json.decode(utf8.decode(response.bodyBytes))['detail']};
      } else {
        return {'status': response.statusCode, 'detail': json.decode(response.body)['detail']};
      }
    } catch (e) {
      return {'status': 404, 'detail': 'Network error: ${e.toString()}'};
    }
  }
}
