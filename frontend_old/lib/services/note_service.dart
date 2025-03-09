import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/note.dart';
import '../models/user.dart';
import 'auth_service.dart';

class NoteService {
  static const String baseUrl = 'http://10.0.2.2:8000/api/notes';
  final AuthService _authService;

  NoteService(this._authService);

  static Future<NoteService> create() async {
    final authService = await AuthService.create();
    return NoteService(authService);
  }

  Future<Map<String, dynamic>> getNotes() async {
    try {
      final response = await _authService.authenticatedRequest(() => http.get(
            Uri.parse('$baseUrl/get'),
            headers: {
              'Authorization': 'Bearer ${_authService.getToken()}',
            },
          ).timeout(Duration(seconds: 3)));

      if (response.statusCode == 200) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        final notes = data.map((note) => Note.fromJson(note)).toList();
        return {'notes': notes, 'status': 200, 'detail': null};
      } else {
        return {'notes': [], 'status': response.statusCode, 'detail': json.decode(response.body)['detail']};
      }
    } catch (e) {
      return {'notes': [], 'status': 404, 'detail': 'Timeout error'};
    }
  }

  Future<Map<String, dynamic>> createNote(Note note) async {
    try {
      Map<String, dynamic> formData = {
        'title': note.title,
        'text': note.text,
        'plant_id': note.plantId,
        'day': note.day.toIso8601String(),
      };
      final response = await _authService.authenticatedRequest(() => http
          .post(
            Uri.parse('$baseUrl/create'),
            headers: {
              'Authorization': 'Bearer ${_authService.getToken()}',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
            body: formData,
          )
          .timeout(Duration(seconds: 3)));

      if (response.statusCode == 201) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        return {'note': Note.fromJson(data['note']), 'status': 201, 'detail': null};
      } else {
        return {'note': null, 'status': response.statusCode, 'detail': json.decode(response.body)['detail']};
      }
    } catch (e) {
      return {'note': null, 'status': 404, 'detail': 'Timeout error'};
    }
  }

  Future<Map<String, dynamic>> deleteNote(Note note) async {
    try {
      final response = await _authService.authenticatedRequest(() => http.delete(
            Uri.parse('$baseUrl/delete/${note.id}'),
            headers: {
              'Authorization': 'Bearer ${_authService.getToken()}',
            },
          ).timeout(Duration(seconds: 3)));

      if (response.statusCode == 200) {
        return {'status': 200, 'detail': null};
      } else {
        return {'status': response.statusCode, 'detail': json.decode(response.body)['detail']};
      }
    } catch (e) {
      return {'status': 404, 'detail': 'Timeout error'};
    }
  }
}
