import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';
import '../models/note.dart';
import '../services/note_service.dart';
import '../services/auth_service.dart';
import '../pages/home_page.dart';
import '../pages/widgets/notecard.dart';
import '../pages/general/bottom_navigator.dart';

class NotesPage extends StatefulWidget {
  @override
  State<NotesPage> createState() => _NotesPageState();
}

class _NotesPageState extends State<NotesPage> {
  late AuthService _authService;
  late NoteService _noteService;
  List<Note> notes = [];
  bool isLoading = false;
  String? error;

  @override
  void initState() {
    super.initState();
    _initServices();
  }

  Future<void> _initServices() async {
    setState(() {
      isLoading = true;
    });

    try {
      _authService = await AuthService.create();
      _noteService = await NoteService.create();
      await _fetchNotes();
    } catch (e) {
      setState(() {
        error = 'Ошибка инициализации: $e';
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  Future<void> _fetchNotes() async {
    try {
      final response = await _noteService.getNotes();
      if (response['status'] == 200) {
        setState(() {
          notes = response['notes'];
          error = null;
        });
      } else {
        setState(() {
          error = response['detail'];
        });
      }
    } catch (e) {
      setState(() {
        error = 'Ошибка загрузки заметок: $e';
      });
    }
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
                      'Заметки',
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
            if (isLoading)
              const Center(child: CircularProgressIndicator())
            else if (error != null)
              Center(child: Text(error!))
            else
              ListView.builder(
                itemCount: notes.length,
                itemBuilder: (context, index) {
                  return NoteCard(note: notes[index]);
                },
              ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigator(),
    );
  }
}
