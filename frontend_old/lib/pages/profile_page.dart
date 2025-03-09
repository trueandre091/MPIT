import 'package:flutter/material.dart';
import 'package:frontend/pages/login_page.dart';
import '../services/auth_service.dart';
import 'home_page.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  _ProfilePageState createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  late AuthService _authService;
  String? userEmail;
  String? userName;
  String? userRole;

  @override
  void initState() {
    super.initState();
    _initService();
  }

  Future<void> _initService() async {
    _authService = await AuthService.create();
    final response = await _authService.me();
    final user = response['user'];
    if (user != null) {
      setState(() {
        userEmail = user.email;
        userRole = user.role;
        userName = user.name;
      });
    } else {
      _authService.logout();
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (context) => const LoginPage()),
        (route) => false,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).primaryColorLight,
      appBar: AppBar(
        toolbarHeight: 30,
        backgroundColor: Theme.of(context).primaryColorLight,
      ),
      body: Center(
        child: Padding(
          padding: EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 0.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: EdgeInsets.only(top: 10.0),
                      child: Text(
                        'Профиль',
                        style: Theme.of(context).textTheme.displaySmall,
                      ),
                    ),
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
              SizedBox(height: 20),
              Container(
                padding: EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Theme.of(context).focusColor,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Добро пожаловать,\n${userName ?? 'Пользователь'}!',
                          style: TextStyle(
                            color: Theme.of(context).cardColor,
                            fontSize: 24,
                            fontFamily: 'Mulish',
                            height: 1.2,
                          ),
                        ),
                        Container(
                          width: 50,
                          height: 50,
                          decoration: BoxDecoration(
                            color: Theme.of(context).cardColor.withAlpha(150),
                            borderRadius: BorderRadius.circular(15),
                          ),
                          child: Icon(
                            Icons.person_outline,
                            color: Theme.of(context).cardColor,
                            size: 30,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 20),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'e-mail:',
                          style: TextStyle(
                            color: Theme.of(context).cardColor.withAlpha(150),
                            fontSize: 16,
                            fontFamily: 'Mulish',
                          ),
                        ),
                        Text(
                          userEmail ?? '-',
                          style: TextStyle(
                            color: Theme.of(context).cardColor,
                            fontSize: 18,
                            fontFamily: 'Mulish',
                          ),
                        ),
                        SizedBox(height: 10),
                        Text(
                          'имя:',
                          style: TextStyle(
                            color: Theme.of(context).cardColor.withAlpha(150),
                            fontSize: 16,
                            fontFamily: 'Mulish',
                          ),
                        ),
                        Text(
                          userName ?? '-',
                          style: TextStyle(
                            color: Theme.of(context).cardColor,
                            fontSize: 18,
                            fontFamily: 'Mulish',
                          ),
                        ),
                        SizedBox(height: 10),
                        Text(
                          'статус пользователя:',
                          style: TextStyle(
                            color: Theme.of(context).cardColor.withAlpha(150),
                            fontSize: 16,
                            fontFamily: 'Mulish',
                          ),
                        ),
                        Text(
                          userRole ?? '-',
                          style: TextStyle(
                            color: Theme.of(context).cardColor,
                            fontSize: 18,
                            fontFamily: 'Mulish',
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 20),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        ElevatedButton(
                          onPressed: () {
                            // Добавить функционал редактирования
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Theme.of(context).cardColor,
                            foregroundColor: Theme.of(context).highlightColor,
                            padding: EdgeInsets.symmetric(vertical: 15),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(15),
                            ),
                          ),
                          child: Text(
                            'Редактировать профиль',
                            style: TextStyle(
                              fontSize: 18,
                              fontFamily: 'Mulish',
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                        SizedBox(height: 10),
                        ElevatedButton.icon(
                          onPressed: () {},
                          icon: Icon(Icons.security),
                          label: Text(
                            'Управление сессиями',
                            style: TextStyle(
                              fontSize: 18,
                              fontFamily: 'Mulish',
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Theme.of(context).cardColor,
                            foregroundColor: Theme.of(context).highlightColor,
                            padding: EdgeInsets.symmetric(vertical: 15),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(15),
                            ),
                          ),
                        ),
                        SizedBox(height: 10),
                        ElevatedButton.icon(
                          onPressed: () {
                            _authService.logout();
                            Navigator.pushAndRemoveUntil(
                              context,
                              MaterialPageRoute(builder: (context) => const LoginPage()),
                              (route) => false,
                            );
                          },
                          icon: Icon(
                            Icons.logout,
                            color: Theme.of(context).cardColor,
                            size: 24,
                          ),
                          label: Text(
                            'Выйти',
                            style: TextStyle(
                              fontSize: 18,
                              fontFamily: 'Mulish',
                              fontWeight: FontWeight.bold,
                              color: Theme.of(context).cardColor,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
