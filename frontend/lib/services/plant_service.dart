import 'package:http/http.dart' as http;
import '../models/plant.dart';
import '../services/auth_service.dart';

class PlantService {
  final String _baseUrl = 'http://10.0.2.2:8000/api/plants';
  final AuthService _authService;

  PlantService(this._authService);

  Future<List<Plant>> getPlants() async {
    final token = _authService.getToken();
    if (token == null) {
      throw Exception('Не авторизован');
    }

    try {
      final response = await http
          .get(Uri.parse('$_baseUrl/get'), headers: {'Authorization': 'Bearer $token'}).timeout(Duration(seconds: 5));
      if (response.statusCode == 200) {
        return (response.body as List).map((e) => Plant.fromJson(e)).toList();
      } else if (response.statusCode == 404) {
        return [];
      } else {
        throw Exception('Failed to load plants');
      }
    } catch (e) {
      throw Exception('Failed to load plants: $e');
    }
  }
}
