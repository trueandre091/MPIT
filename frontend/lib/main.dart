import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'styles/themes.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'pages/home_page.dart';
import 'package:google_fonts/google_fonts.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeDateFormatting('ru_RU', null);
  
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);

  await GoogleFonts.pendingFonts([
    GoogleFonts.mulish(),
    GoogleFonts.museoModerno(),
  ]);

  runApp(MaterialApp(
    home: HomePage(),
    title: 'Flora Friend',
    theme: appTheme(),
    localizationsDelegates: const [
      GlobalMaterialLocalizations.delegate,
      GlobalWidgetsLocalizations.delegate,
      GlobalCupertinoLocalizations.delegate,
    ],
    supportedLocales: const [
      Locale('ru', 'RU'),
    ],
  ));
}
