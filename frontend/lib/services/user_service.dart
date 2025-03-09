import 'package:http/http.dart' as http;
import '../models/user.dart';
import '../services/auth_service.dart';

class UserService {
  static const String baseUrl = 'http://10.0.2.2:8000/api/users';
  final AuthService _authService;

  UserService(this._authService);

  Future<User> getUser() async {
    try {
      final response = await _authService.me();
      if (response['status'] == 200) {
        return response['user'];
      } else if (response['status'] == 401 || response['status'] == 403) {
        await _authService.clearToken();
        throw Exception('Не авторизован');
      } else {
        throw Exception('Не удалось загрузить пользователя');
      }
    } catch (e) {
      throw Exception('Не удалось загрузить пользователя');
    }
  }
}
