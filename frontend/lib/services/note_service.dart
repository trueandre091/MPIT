import 'package:http/http.dart' as http;
import '../models/note.dart';
import '../services/auth_service.dart';
import 'dart:convert';
import 'package:http_parser/http_parser.dart';
import 'dart:convert' show utf8;

class NoteService {
  static const String baseUrl = 'http://10.0.2.2:8000/api/notes';
  final AuthService _authService;

  NoteService(this._authService);

  Future<List<Note>> getNotes() async {
    final token = _authService.getToken();
    if (token == null) {
      throw Exception('Не авторизован');
    }
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/get'),
        headers: {'Authorization': 'Bearer $token'},
      ).timeout(Duration(seconds: 3));

      if (response.statusCode == 200) {
        final decodedResponse = utf8.decode(response.bodyBytes);
        return (jsonDecode(decodedResponse)['notes'] as List).map((e) => Note.fromJson(e)).toList();
      } else if (response.statusCode == 401) {
        _authService.clearToken();
        throw Exception('Не авторизован');
      } else {
        throw Exception('Не удалось загрузить заметки');
      }
    } catch (e) {
      throw Exception('Не удалось загрузить заметки: $e');
    }
  }

  Future<Note> createNote(Note note) async {
    final token = _authService.getToken();
    if (token == null) {
      throw Exception('Не авторизован');
    }

    try {
      final Map<String, String> headers = {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/x-www-form-urlencoded',
      };

      final Map<String, dynamic> formData = {
        'title': note.title,
        'text': note.text,
      };

      if (note.plantId != null) {
        formData['plant_id'] = note.plantId!.toString();
      }

      if (note.day != null) {
        formData['day'] = note.day!.toIso8601String();
      }

      final response = await http
          .post(
            Uri.parse('$baseUrl/create'),
            headers: headers,
            body: formData,
          )
          .timeout(Duration(seconds: 3));

      if (response.statusCode == 201) {
        final decodedResponse = utf8.decode(response.bodyBytes);
        final responseData = jsonDecode(decodedResponse);
        if (responseData['note'] != null) {
          return Note.fromJson(responseData['note']);
        } else {
          throw Exception('Некорректный ответ от сервера');
        }
      } else if (response.statusCode == 401) {
        _authService.clearToken();
        throw Exception('Не авторизован');
      } else {
        final decodedError = utf8.decode(response.bodyBytes);
        throw Exception('Не удалось создать заметку: $decodedError');
      }
    } catch (e) {
      throw Exception('Ошибка при создании заметки: $e');
    }
  }

  Future<void> deleteNote(String id) async {
    final token = _authService.getToken();
    if (token == null) {
      throw Exception('Не авторизован');
    }

    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/delete/$id'),
        headers: {'Authorization': 'Bearer $token'},
      ).timeout(Duration(seconds: 3));

      if (response.statusCode == 200) {
        return;
      } else if (response.statusCode == 401) {
        _authService.clearToken();
        throw Exception('Не авторизован');
      } else if (response.statusCode == 404) {
        throw Exception('Заметка не найдена');
      } else {
        throw Exception(response.body);
      }
    } catch (e) {
      throw Exception('Ошибка при удалении заметки: $e');
    }
  }

  Future<Note> editNote(int id, String? title, String? text, int? plantId, DateTime? day) async {
    final token = _authService.getToken();
    if (token == null) {
      throw Exception('Не авторизован');
    }

    final Map<String, dynamic> formData = {};
    if (title != null) {
      formData['title'] = title;
    }
    if (text != null) {
      formData['text'] = text;
    }
    if (plantId != null) {
      formData['plant_id'] = plantId.toString();
    }
    if (day != null) {
      formData['day'] = day.toIso8601String();
    }

    try {
      final response = await http.patch(
        Uri.parse('$baseUrl/update/$id'),
        headers: {'Authorization': 'Bearer $token'},
        body: formData,
      );

      if (response.statusCode == 200) {
        final decodedResponse = utf8.decode(response.bodyBytes);
        final responseData = jsonDecode(decodedResponse);
        return Note.fromJson(responseData['note']);
      } else if (response.statusCode == 401) {
        _authService.clearToken();
        throw Exception('Не авторизован');
      } else {
        throw Exception(response.body);
      }
    } catch (e) {
      throw Exception('Ошибка при редактировании заметки: $e');
    }
  }
}
