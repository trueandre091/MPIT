import 'package:flutter/material.dart';

ThemeData appTheme() {
  return ThemeData(
    appBarTheme: const AppBarTheme(
      backgroundColor: Colors.white,
      foregroundColor: Colors.black,
    ),
    inputDecorationTheme: const InputDecorationTheme(
      fillColor: Colors.white,
      filled: true,
    ),
    dialogTheme: const DialogTheme(
      backgroundColor: Colors.white,
      surfaceTintColor: Colors.white,
    ),
    splashFactory: NoSplash.splashFactory,
    primaryColorDark: Colors.black,
    primaryColorLight: Colors.white,
    scaffoldBackgroundColor: Colors.white,
    shadowColor: Color.fromRGBO(97, 160, 88, 1),
    focusColor: Color.fromRGBO(248, 214, 210, 1),
    highlightColor: Color.fromRGBO(236, 132, 130, 1),
    canvasColor: Color.fromRGBO(97, 160, 88, 1),
    cardColor: Color.fromRGBO(99, 119, 85, 1),
  );
}
