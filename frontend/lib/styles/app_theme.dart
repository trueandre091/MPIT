import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:google_fonts/google_fonts.dart';

class ThemeProvider with ChangeNotifier {
  bool _isDarkMode = false;

  // Геттер для текущего состояния темы
  bool get isDarkMode => _isDarkMode;

  // Конструктор для загрузки сохранённой темы
  ThemeProvider() {
    _loadTheme();
  }

  // Метод для переключения темы
  void toggleTheme() async {
    _isDarkMode = !_isDarkMode;
    await _saveTheme(); // Сохраняем новое состояние
    notifyListeners(); // Уведомляем подписчиков об изменении
  }

  // Метод для загрузки сохранённой темы
  Future<void> _loadTheme() async {
    final prefs = await SharedPreferences.getInstance();
    _isDarkMode = prefs.getBool('isDarkMode') ?? false; // Значение по умолчанию: false
    notifyListeners();
  }

  // Метод для сохранения текущей темы
  Future<void> _saveTheme() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('isDarkMode', _isDarkMode);
  }
}

class AppThemes {
  static final lightTheme = ThemeData(
    // яркость
    brightness: Brightness.light,
    // цвет
    primaryColor: const Color.fromARGB(255, 109, 235, 93),
    // схема цветов
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color.fromARGB(255, 109, 235, 93),
      brightness: Brightness.light,
    ),

    // текст
    textTheme: TextTheme(
      titleLarge: GoogleFonts.montserrat(
        fontSize: 24,
        fontWeight: FontWeight.w500,
      ),
      // заголовок
      displayLarge: GoogleFonts.montserrat(fontSize: 24, fontWeight: FontWeight.bold),
      // текст
      bodyLarge: GoogleFonts.montserrat(fontSize: 16, color: Colors.black),
    ),
  );

  static final darkTheme = ThemeData(
    brightness: Brightness.dark,
    primaryColor: const Color.fromARGB(255, 117, 204, 105),
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color.fromARGB(255, 117, 204, 105),
      brightness: Brightness.dark,
    ),
    textTheme: TextTheme(
      titleLarge: GoogleFonts.montserrat(
        fontSize: 24,
        fontWeight: FontWeight.w500,
      ),
      displayLarge: GoogleFonts.montserrat(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white),
      bodyLarge: GoogleFonts.montserrat(fontSize: 16, color: Colors.white),
    ),
  );
}
