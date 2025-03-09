import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../services/auth_service.dart';
import 'dart:convert';
import 'home_page.dart';
import 'profile_page.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _nameController = TextEditingController();
  bool _isLoading = false;
  bool _isRegistration = false;
  late AuthService _authService;

  @override
  void initState() {
    super.initState();
    _initService();
  }

  Future<void> _initService() async {
    _authService = await AuthService.create();
    final isAuthenticated = await _authService.isAuthenticated();
    if (isAuthenticated) {
      if (mounted) {
        Navigator.pushAndRemoveUntil(
          context,
          MaterialPageRoute(builder: (context) => const ProfilePage()),
          (route) => false,
        );
      }
    }
  }

  String extractErrorMessages(dynamic data) {
    List<String> errors = [];

    if (data is List) {
      // Если данные — это список, обрабатываем каждый элемент
      for (var item in data) {
        if (item is String) {
          // Если элемент — строка, добавляем его напрямую
          errors.add(item);
        } else if (item is Map) {
          // Если элемент — Map, вызываем функцию рекурсивно
          errors.addAll(extractErrorMessages(item).split('\n'));
        }
      }
    } else if (data is Map) {
      // Если данные — это Map, обрабатываем ключи и значения
      data.forEach((key, value) {
        if (value is List) {
          // Если значение — это список ошибок
          for (var error in value) {
            errors.add('$key: $error');
          }
        } else if (value is Map) {
          // Если значение — это еще один Map, вызываем функцию рекурсивно
          errors.addAll(extractErrorMessages(value).split('\n'));
        }
      });
    }

    // Возвращаем все ошибки как одну строку, разделенную переносом строки
    return errors.join('\n');
  }

  void _showErrorMessage(String message) {
    // Закрываем клавиатуру перед показом ошибки
    FocusScope.of(context).unfocus();

    ScaffoldMessenger.of(context)
      ..clearSnackBars()
      ..showSnackBar(
        SnackBar(
          content: Text(
            message,
            style: TextStyle(
              color: Colors.white,
              fontFamily: 'Mulish',
              fontSize: 16,
            ),
          ),
          backgroundColor: Colors.red,
          behavior: SnackBarBehavior.floating,
          margin: EdgeInsets.only(
            top: 70,
            left: 20,
            right: 20,
          ),
          dismissDirection: DismissDirection.horizontal,
          duration: Duration(seconds: 3),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15),
          ),
        ),
      );
  }

  Future<void> _login() async {
    if (_emailController.text.isEmpty || _passwordController.text.isEmpty) return;
    if (_isRegistration && _nameController.text.isEmpty) return;

    setState(() {
      _isLoading = true;
    });

    try {
      Map<String, dynamic> response;
      if (_isRegistration) {
        response = await _authService.register(
          _emailController.text,
          _passwordController.text,
          _nameController.text,
        );
      } else {
        response = await _authService.login(
          _emailController.text,
          _passwordController.text,
        );
      }
      print(response);
      if (response['status'] == 200 || response['status'] == 201) {
        Navigator.pushAndRemoveUntil(
          context,
          MaterialPageRoute(builder: (context) => const ProfilePage()),
          (route) => false,
        );
      } else {
        _showErrorMessage(
            response['detail'].runtimeType == String ? response['detail'] : extractErrorMessages(response['detail']));
      }
    } catch (e) {
      return;
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _toggleMode() {
    setState(() {
      _isRegistration = !_isRegistration;
      _emailController.clear();
      _passwordController.clear();
      _nameController.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    final keyboardHeight = MediaQuery.of(context).viewInsets.bottom;
    return Scaffold(
      resizeToAvoidBottomInset: false,
      backgroundColor: Theme.of(context).primaryColorLight,
      body: SafeArea(
        child: Container(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 0.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    IconButton(
                      onPressed: () {
                        Navigator.pushAndRemoveUntil(
                          context,
                          MaterialPageRoute(builder: (context) => const HomePage()),
                          (route) => false,
                        );
                      },
                      icon: Icon(
                        Icons.house_outlined,
                        size: 50,
                        color: Theme.of(context).cardColor,
                      ),
                    ),
                  ],
                ),
              ),
              Expanded(
                flex: 3,
                child: Padding(
                  padding: EdgeInsets.symmetric(horizontal: 30.0, vertical: 0.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Добро пожаловать в',
                        style: TextStyle(
                          color: Theme.of(context).cardColor,
                          fontSize: 24,
                          fontFamily: 'Mulish',
                        ),
                      ),
                      Text(
                        'Flora\nFriend',
                        style: TextStyle(
                          fontFamily: 'MuseoModerno',
                          fontSize: 70,
                          height: 1,
                          color: Theme.of(context).cardColor,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              Expanded(
                flex: keyboardHeight > 0 ? 10 : 3,
                child: Container(
                  padding: EdgeInsets.symmetric(horizontal: 20, vertical: 20),
                  decoration: BoxDecoration(
                    color: Theme.of(context).cardColor,
                    borderRadius: BorderRadius.only(topLeft: Radius.circular(30), topRight: Radius.circular(30)),
                  ),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Padding(
                      padding: EdgeInsets.only(bottom: 20, left: 10),
                      child: Text(
                        _isRegistration ? 'Регистрация:' : 'Войти в аккаунт:',
                        style: TextStyle(
                          color: Theme.of(context).primaryColorLight,
                          fontSize: 24,
                          letterSpacing: 1,
                          fontFamily: 'Mulish',
                          fontWeight: FontWeight.normal,
                        ),
                      ),
                    ),
                    if (_isRegistration)
                      Container(
                        margin: EdgeInsets.only(bottom: 20),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(30),
                        ),
                        child: TextField(
                          controller: _nameController,
                          textInputAction: TextInputAction.next,
                          keyboardType: TextInputType.name,
                          style: TextStyle(
                            fontFamily: 'Mulish',
                            fontSize: 20,
                            fontWeight: FontWeight.normal,
                          ),
                          decoration: InputDecoration(
                            hintText: 'введите полное имя...',
                            hintStyle: TextStyle(
                              color: Colors.grey,
                              fontFamily: 'Mulish',
                              fontSize: 20,
                              fontWeight: FontWeight.normal,
                            ),
                            prefixIcon: Icon(Icons.person_outline),
                            border: InputBorder.none,
                            contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
                          ),
                        ),
                      ),
                    Container(
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(30),
                      ),
                      child: TextField(
                        controller: _emailController,
                        textInputAction: TextInputAction.next,
                        keyboardType: TextInputType.emailAddress,
                        style: TextStyle(
                          fontFamily: 'Mulish',
                          fontSize: 20,
                          fontWeight: FontWeight.normal,
                        ),
                        decoration: InputDecoration(
                          hintText: 'введите электронную почту...',
                          hintStyle: TextStyle(
                            color: Colors.grey,
                            fontFamily: 'Mulish',
                            fontSize: 20,
                            fontWeight: FontWeight.normal,
                          ),
                          prefixIcon: Icon(Icons.mail_outline),
                          border: InputBorder.none,
                          contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
                        ),
                      ),
                    ),
                    SizedBox(height: 20),
                    Container(
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(30),
                      ),
                      child: TextField(
                        controller: _passwordController,
                        textInputAction: TextInputAction.done,
                        keyboardType: TextInputType.visiblePassword,
                        obscureText: true,
                        style: TextStyle(
                          fontFamily: 'Mulish',
                          fontSize: 20,
                          fontWeight: FontWeight.normal,
                        ),
                        onSubmitted: (_) => _login(),
                        decoration: InputDecoration(
                          hintText: 'введите пароль...',
                          hintStyle: TextStyle(
                            color: Colors.grey,
                            fontFamily: 'Mulish',
                            fontSize: 20,
                            fontWeight: FontWeight.normal,
                          ),
                          prefixIcon: Icon(Icons.lock_outline),
                          border: InputBorder.none,
                          contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
                        ),
                      ),
                    ),
                    SizedBox(height: 20),
                    Row(
                      children: [
                        Expanded(
                          child: ElevatedButton(
                            onPressed: _isLoading ? null : _login,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Theme.of(context).highlightColor,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(30),
                              ),
                              padding: EdgeInsets.symmetric(vertical: 15),
                            ),
                            child: _isLoading
                                ? SizedBox(
                                    height: 20,
                                    width: 20,
                                    child: CircularProgressIndicator(
                                      strokeWidth: 2,
                                      color: Colors.white,
                                    ),
                                  )
                                : Text(
                                    _isRegistration ? 'Зарегистрироваться' : 'Войти',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 18,
                                      fontFamily: 'Mulish',
                                    ),
                                  ),
                          ),
                        ),
                        SizedBox(width: 10),
                        Expanded(
                          child: ElevatedButton(
                            onPressed: _toggleMode,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.transparent,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(30),
                                side: BorderSide(color: Theme.of(context).highlightColor),
                              ),
                              padding: EdgeInsets.symmetric(vertical: 15),
                            ),
                            child: Text(
                              _isRegistration ? 'Войти' : 'Регистрация',
                              style: TextStyle(
                                color: Theme.of(context).highlightColor,
                                fontSize: 18,
                                fontFamily: 'Mulish',
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ]),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _nameController.dispose();
    super.dispose();
  }
}
