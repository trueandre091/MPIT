import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'home_page.dart';
import '../services/auth_service.dart';
import 'general/bottom_navigator.dart';
import 'dart:convert';

class CameraPage extends StatefulWidget {
  const CameraPage({super.key});

  @override
  _CameraPageState createState() => _CameraPageState();
}

class _CameraPageState extends State<CameraPage> {
  File? _image;
  final ImagePicker _picker = ImagePicker();
  bool _isProcessing = false;
  Map<String, dynamic>? _classificationResult;
  late AuthService _authService;

  @override
  void initState() {
    super.initState();
    _initServices();
  }

  Future<void> _initServices() async {
    _authService = await AuthService.create();
  }

  Future<void> _openCamera() async {
    final XFile? pickedFile = await _picker.pickImage(source: ImageSource.camera);
    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
        _classificationResult = null;
      });
    }
  }

  Future<void> _classifyPlant() async {
    if (_image == null) return;

    setState(() {
      _isProcessing = true;
    });

    // Имитация задержки обработки
    await Future.delayed(Duration(seconds: 2));

    setState(() {
      _isProcessing = false;
      _classificationResult = {
        'status': 200,
        'result': {
          'name': 'Демо-растение',
          'description': 'Это демонстрационный режим. Функция определения растений будет доступна позже.'
        },
      };
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      backgroundColor: Theme.of(context).primaryColorLight,
      appBar: AppBar(
        toolbarHeight: 30,
        backgroundColor: Theme.of(context).primaryColorLight,
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Container(
              padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 0.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Padding(
                    padding: EdgeInsets.only(top: 10.0),
                    child: Text(
                      'Камера',
                      style: Theme.of(context).textTheme.displaySmall,
                    ),
                  ),
                  Container(
                    padding: EdgeInsets.only(right: 10.0),
                    child: IconButton(
                      onPressed: () {
                        Navigator.pushReplacement(
                          context,
                          MaterialPageRoute(builder: (context) => const HomePage()),
                        );
                      },
                      icon: Icon(
                        Icons.house_outlined,
                        size: 50,
                        color: Theme.of(context).cardColor,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            Expanded(
              child: _image == null
                  ? Column(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Фото не выбрано',
                          style: Theme.of(context).textTheme.bodyMedium,
                        ),
                      ],
                    )
                  : SingleChildScrollView(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          Image.file(_image!),
                          SizedBox(height: 20),
                          if (_classificationResult == null)
                            ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Theme.of(context).highlightColor,
                                foregroundColor: Theme.of(context).cardColor,
                              ),
                              onPressed: _isProcessing ? null : _classifyPlant,
                              child: _isProcessing
                                  ? SizedBox(
                                      height: 20,
                                      width: 20,
                                      child: CircularProgressIndicator(
                                        color: Colors.white,
                                        strokeWidth: 2,
                                      ),
                                    )
                                  : Text(
                                      'Определить растение',
                                      style: Theme.of(context).textTheme.bodyMedium,
                                    ),
                            ),
                          if (_classificationResult != null) _buildResultWidget(),
                        ],
                      ),
                    ),
            ),
            if (_classificationResult == null)
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Theme.of(context).primaryColor,
                  foregroundColor: Theme.of(context).cardColor,
                ),
                onPressed: _openCamera,
                child: Text(
                  'Сделать фото',
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigator(),
    );
  }

  Widget _buildResultWidget() {
    if (_classificationResult == null) return SizedBox.shrink();

    if (_classificationResult!['status'] != 200) {
      return Container(
        margin: EdgeInsets.symmetric(vertical: 20),
        padding: EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.red.shade50,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: Colors.red.shade200),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Ошибка при определении:',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: Colors.red.shade800,
                fontSize: 16,
              ),
            ),
            SizedBox(height: 8),
            Text(
              _classificationResult!['error'] ?? 'Неизвестная ошибка',
              style: TextStyle(color: Colors.red.shade700),
            ),
          ],
        ),
      );
    }

    // Успешный результат
    final result = _classificationResult!['result'];

    return Container(
      margin: EdgeInsets.symmetric(vertical: 20),
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.green.shade50,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.green.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Результат определения:',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 18,
              color: Colors.green.shade800,
            ),
          ),
          SizedBox(height: 12),

          // Название растения
          _buildResultRow(
            'Название:',
            result['name'],
          ),

          // Описание
          _buildResultRow(
            'Описание:',
            result['description'],
          ),
        ],
      ),
    );
  }

  Widget _buildResultRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 16,
            ),
          ),
          SizedBox(width: 8),
          Expanded(
            child: Text(
              value,
              style: TextStyle(fontSize: 16),
            ),
          ),
        ],
      ),
    );
  }
}
