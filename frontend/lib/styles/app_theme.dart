import 'package:flutter/material.dart';

ThemeData appTheme() {
  return ThemeData(
    splashFactory: NoSplash.splashFactory,

    // Цветовая палитра
    primaryColor: Color.fromRGBO(99, 119, 85, 1),
    shadowColor: Color.fromRGBO(49, 61, 48, 1),
    focusColor: Color.fromRGBO(248, 214, 210, 1),
    highlightColor: Color.fromRGBO(236, 132, 130, 1),
    canvasColor: Color.fromRGBO(249, 241, 206, 1),
    splashColor: Colors.transparent,

    primaryColorLight: Colors.white,
    primaryColorDark: Color.fromRGBO(44, 40, 40, 1),
    cardColor: Colors.black,

    // Стили текста
    textTheme: TextTheme(
      displayLarge: TextStyle(
        fontSize: 60.0,
        fontFamily: 'Mulish',
        fontWeight: FontWeight.bold,
        color: Color.fromRGBO(44, 40, 40, 1),
      ),
      displayMedium: TextStyle(
        fontSize: 48.0,
        fontFamily: 'Mulish',
        fontWeight: FontWeight.bold,
        color: Color.fromRGBO(44, 40, 40, 1),
      ),
      displaySmall: TextStyle(
        fontSize: 36.0,
        fontFamily: 'Mulish',
        fontWeight: FontWeight.bold,
        color: Color.fromRGBO(44, 40, 40, 1),
      ),
      labelLarge: TextStyle(
        fontSize: 24.0,
        fontFamily: 'Mulish',
        fontWeight: FontWeight.normal,
        color: Color.fromRGBO(44, 40, 40, 1),
      ),
      labelMedium: TextStyle(
        fontSize: 20.0,
        fontFamily: 'Mulish',
        fontWeight: FontWeight.normal,
        color: Color.fromRGBO(44, 40, 40, 1),
      ),
      labelSmall: TextStyle(
        fontSize: 16.0,
        fontFamily: 'Mulish',
        fontWeight: FontWeight.normal,
        color: Color.fromRGBO(44, 40, 40, 1),
      ),
      bodyLarge: TextStyle(
        fontSize: 30.0,
        fontFamily: 'Mulish',
        fontWeight: FontWeight.bold,
        color: Color.fromRGBO(44, 40, 40, 1),
      ),
      bodyMedium: TextStyle(
        fontSize: 20.0,
        fontFamily: 'Mulish',
        fontWeight: FontWeight.bold,
        color: Color.fromRGBO(44, 40, 40, 1),
      ),
      bodySmall: TextStyle(
        fontSize: 10.0,
        fontFamily: 'Mulish',
        fontWeight: FontWeight.bold,
        color: Color.fromRGBO(44, 40, 40, 1),
      ),
      titleLarge: TextStyle(
        fontSize: 40.0,
        fontFamily: 'MuseoModerno',
        fontWeight: FontWeight.bold,
        color: Color.fromRGBO(44, 40, 40, 1),
      ),
      titleMedium: TextStyle(
        fontSize: 20.0,
        fontFamily: 'Mulish',
        color: Color.fromRGBO(44, 40, 40, 1),
      ),
    ),
  );
}
