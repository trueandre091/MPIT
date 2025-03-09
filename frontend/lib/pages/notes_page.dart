import 'package:flutter/material.dart';
import '../widgets/bottom_navigator.dart';
import '../widgets/page_title.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/note.dart';
import '../services/auth_service.dart';
import '../services/note_service.dart';
import '../pages/note_create_page.dart';
import '../pages/login_page.dart';

class NotesPage extends StatefulWidget {
  const NotesPage({super.key});

  @override
  State<NotesPage> createState() => _NotesPageState();
}

class _NotesPageState extends State<NotesPage> {
  late AuthService _authService;
  late NoteService _noteService;
  List<Note> notes = [];
  List<String> days = [];
  bool _isLoading = false;
  String _error = '';
  bool _isAuthenticated = false;

  @override
  void initState() {
    super.initState();
    _initServicesAndLoadNotes();
  }

  Future<void> _initServicesAndLoadNotes() async {
    setState(() {
      _isLoading = true;
    });

    try {
      _authService = await AuthService.create();
      _noteService = NoteService(_authService);
      _isAuthenticated = await _authService.isAuthenticated();
      _isAuthenticated ? await _loadNotes() : _error = "Не авторизован";
      _clearError();
    } catch (e) {
      _error = e.toString();
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _loadNotes() async {
    try {
      notes = await _noteService.getNotes();
      days = notes.map((note) => note.day!.toIso8601String().substring(0, 10)).toSet().toList();
    } catch (e) {
      _error = e.toString();
    }
  }

  Future<void> _clearError() async {
    await Future.delayed(Duration(seconds: 3));
    if (mounted) {
      setState(() {
        _error = '';
      });
    }
  }

  Future<void> _deleteNote(String id) async {
    try {
      await _noteService.deleteNote(id);
      setState(() {
        notes = notes.where((note) => note.id != int.parse(id)).toList();
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
      });
      await _clearError();
    }
  }

  Future<void> _editNote(String id, String? title, String? text, int? plantId, DateTime? day) async {
    try {
      final response = await _noteService.editNote(int.parse(id), title, text, plantId, day);
      setState(() {
        notes = notes.map((note) => note.id.toString() == id ? response : note).toList();
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
      });
      await _clearError();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(toolbarHeight: 30),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30),
        child: Column(
          children: [
            const PageTitle(title: 'Заметки'),
            Expanded(
              child: _isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : ListView.builder(
                      padding: const EdgeInsets.only(bottom: 10, top: 20),
                      itemCount: days.length,
                      itemBuilder: (context, index) {
                        return Container(
                          alignment: Alignment.center,
                          child: Opacity(
                            opacity: 1,
                            child: Container(
                              margin: const EdgeInsets.only(bottom: 20),
                              child: DayNoteCard(
                                day: DateTime.parse(days[index]),
                                notes: notes
                                    .where((note) => note.day!.toIso8601String().substring(0, 10) == days[index])
                                    .toList(),
                                onDelete: (id) {
                                  showDialog(
                                    context: context,
                                    builder: (context) => Dialog(
                                      backgroundColor: Theme.of(context).primaryColorLight,
                                      shape: RoundedRectangleBorder(
                                        borderRadius: BorderRadius.circular(15),
                                      ),
                                      child: Container(
                                        padding: const EdgeInsets.all(20),
                                        child: Column(
                                          mainAxisSize: MainAxisSize.min,
                                          children: [
                                            Text(
                                              'Удалить заметку',
                                              style: GoogleFonts.mulish(
                                                  fontSize: 20,
                                                  fontWeight: FontWeight.bold,
                                                  color: Theme.of(context).primaryColorDark),
                                            ),
                                            const SizedBox(height: 20),
                                            Text(
                                              'Вы уверены, что хотите удалить заметку?',
                                              style: GoogleFonts.mulish(
                                                  fontSize: 16, color: Theme.of(context).primaryColorDark),
                                            ),
                                            const SizedBox(height: 20),
                                            Row(
                                              mainAxisAlignment: MainAxisAlignment.end,
                                              children: [
                                                ElevatedButton(
                                                  onPressed: () async {
                                                    await _deleteNote(id);
                                                    Navigator.pop(context);
                                                  },
                                                  style: ElevatedButton.styleFrom(
                                                    elevation: 0,
                                                    backgroundColor: Theme.of(context).primaryColorLight,
                                                  ),
                                                  child: Text(
                                                    'Удалить',
                                                    style: GoogleFonts.mulish(
                                                        fontSize: 20,
                                                        fontWeight: FontWeight.bold,
                                                        color: Theme.of(context).primaryColorDark),
                                                  ),
                                                ),
                                                const SizedBox(width: 10),
                                                ElevatedButton(
                                                  style: ElevatedButton.styleFrom(
                                                    elevation: 0,
                                                    backgroundColor: Theme.of(context).focusColor,
                                                  ),
                                                  onPressed: () => Navigator.pop(context),
                                                  child: Text(
                                                    'Отменить',
                                                    style: GoogleFonts.mulish(
                                                        fontSize: 20,
                                                        fontWeight: FontWeight.bold,
                                                        color: Theme.of(context).primaryColorDark),
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ],
                                        ),
                                      ),
                                    ),
                                  );
                                },
                                onEdit: (id) {
                                  showDialog(
                                    context: context,
                                    builder: (context) => NoteEditDialog(
                                      note: notes.firstWhere((note) => note.id.toString() == id),
                                      onEdit: (id, title, text, plantId, day) {
                                        _editNote(id.toString(), title, text, plantId, day);
                                      },
                                    ),
                                  );
                                },
                              ),
                            ),
                          ),
                        );
                      },
                    ),
            ),
            _isAuthenticated
                ? Container(
                    margin: const EdgeInsets.only(top: 20),
                    child: ElevatedButton(
                      onPressed: () async {
                        Navigator.pushAndRemoveUntil(
                            context,
                            PageRouteBuilder(
                              pageBuilder: (context, animation, secondaryAnimation) => NoteCreatePage(),
                              transitionDuration: Duration.zero,
                            ),
                            (route) => false);
                      },
                      style: ElevatedButton.styleFrom(
                        elevation: 0,
                        backgroundColor: Theme.of(context).focusColor,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(25),
                        ),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Padding(
                            padding: const EdgeInsets.only(right: 10, bottom: 15, top: 15),
                            child: Text(
                              'Создать заметку',
                              style: GoogleFonts.mulish(
                                  fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorDark),
                            ),
                          ),
                          Icon(Icons.add, color: Theme.of(context).primaryColorDark, size: 30),
                        ],
                      ),
                    ),
                  )
                : Expanded(
                    child: Column(
                      children: [
                        Text("Не авторизован",
                            style: GoogleFonts.mulish(
                                fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorDark)),
                        ElevatedButton(
                            onPressed: () {
                              Navigator.pushAndRemoveUntil(
                                context,
                                MaterialPageRoute(builder: (context) => const LoginPage()),
                                (route) => false,
                              );
                            },
                            style: ElevatedButton.styleFrom(
                              elevation: 0,
                              backgroundColor: Theme.of(context).focusColor,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(25),
                              ),
                            ),
                            child: Text("Войти",
                                style: GoogleFonts.mulish(
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                    color: Theme.of(context).primaryColorDark))),
                      ],
                    ),
                  ),
            if (_error.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 20),
                child: Text(_error,
                    style: GoogleFonts.mulish(
                        fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorDark)),
              ),
          ],
        ),
      ),
      bottomNavigationBar: const BottomNavigator(
        thisIndex: 4,
      ),
    );
  }
}

class DayNoteCard extends StatelessWidget {
  final DateTime day;
  final List<Note> notes;
  final void Function(String) onDelete;
  final void Function(String) onEdit;

  const DayNoteCard({
    super.key,
    required this.day,
    required this.notes,
    required this.onDelete,
    required this.onEdit,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: Theme.of(context).focusColor,
        borderRadius: BorderRadius.circular(25),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Padding(
                padding: const EdgeInsets.only(right: 15),
                child: Text(
                  '${day.toIso8601String().substring(0, 10)}',
                  style: GoogleFonts.mulish(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).primaryColorDark,
                  ),
                ),
              ),
            ],
          ),
          ...notes.map((note) => Container(
                padding: const EdgeInsets.symmetric(vertical: 5, horizontal: 10),
                margin: const EdgeInsets.only(top: 10),
                decoration: BoxDecoration(
                  color: Theme.of(context).primaryColorLight,
                  borderRadius: BorderRadius.circular(15),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    IconButton(
                      onPressed: () {},
                      icon: Container(
                        height: 30,
                        width: 30,
                        decoration: BoxDecoration(
                          color: Theme.of(context).highlightColor,
                          shape: BoxShape.circle,
                        ),
                      ),
                    ),
                    Expanded(
                      child: Padding(
                        padding: const EdgeInsets.only(right: 10),
                        child: Text(
                          note.title,
                          style: GoogleFonts.mulish(
                            fontSize: 16,
                            color: Theme.of(context).primaryColorDark,
                          ),
                        ),
                      ),
                    ),
                    IconButton(
                      alignment: Alignment.centerLeft,
                      icon: Icon(
                        Icons.delete_outlined,
                        size: 24,
                        color: Theme.of(context).primaryColorDark,
                      ),
                      onPressed: () => onDelete(note.id.toString()),
                    ),
                    IconButton(
                      icon: Icon(
                        Icons.edit_outlined,
                        color: Theme.of(context).primaryColorDark,
                      ),
                      onPressed: () => onEdit(note.id.toString()),
                    ),
                  ],
                ),
              )),
        ],
      ),
    );
  }
}

class NoteEditDialog extends StatefulWidget {
  final Note note;
  final void Function(int, String?, String?, int?, DateTime?) onEdit;

  const NoteEditDialog({
    super.key,
    required this.note,
    required this.onEdit,
  });

  @override
  State<NoteEditDialog> createState() => _NoteEditDialogState();
}

class _NoteEditDialogState extends State<NoteEditDialog> {
  TextEditingController _titleController = TextEditingController();
  TextEditingController _textController = TextEditingController();
  TextEditingController _dayController = TextEditingController();
  int? _plantId;
  DateTime? _day;

  @override
  void initState() {
    super.initState();
    _titleController.text = widget.note.title;
    _textController.text = widget.note.text;
    _plantId = widget.note.plantId;
    _day = widget.note.day;
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Theme.of(context).primaryColorLight,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15),
      ),
      child: Container(
        width: MediaQuery.of(context).size.width * 0.8,
        constraints: BoxConstraints(
          maxHeight: MediaQuery.of(context).size.height * 0.7,
        ),
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Редактировать заметку',
              style: GoogleFonts.mulish(
                  fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorDark),
            ),
            const SizedBox(height: 20),
            Flexible(
              child: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      margin: const EdgeInsets.only(bottom: 20),
                      child: TextField(
                        controller: _titleController,
                        style: GoogleFonts.mulish(
                          fontSize: 18,
                          color: Theme.of(context).primaryColorDark,
                        ),
                        decoration: InputDecoration(
                          hintText: 'Заголовок',
                          filled: true,
                          fillColor: Theme.of(context).primaryColorLight,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(15),
                            borderSide: BorderSide.none,
                          ),
                          contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
                        ),
                      ),
                    ),
                    Container(
                      margin: const EdgeInsets.only(bottom: 20),
                      child: TextField(
                        controller: _textController,
                        maxLines: 4,
                        style: GoogleFonts.mulish(
                          fontSize: 18,
                          color: Theme.of(context).primaryColorDark,
                        ),
                        decoration: InputDecoration(
                          hintText: 'Текст заметки',
                          filled: true,
                          fillColor: Theme.of(context).primaryColorLight,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(15),
                            borderSide: BorderSide.none,
                          ),
                          contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
                        ),
                      ),
                    ),
                    Container(
                      margin: const EdgeInsets.only(bottom: 20),
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 5),
                      decoration: BoxDecoration(
                        color: Theme.of(context).primaryColorLight,
                        borderRadius: BorderRadius.circular(15),
                      ),
                      child: DropdownButton<int>(
                        value: _plantId,
                        isExpanded: true,
                        underline: Container(),
                        hint: Text(
                          'Выберите растение',
                          style: GoogleFonts.mulish(
                            fontSize: 18,
                            color: Theme.of(context).primaryColorDark,
                          ),
                        ),
                        onChanged: (newValue) {
                          setState(() {
                            _plantId = newValue;
                          });
                        },
                        items: [],
                      ),
                    ),
                    Container(
                      margin: const EdgeInsets.only(bottom: 20),
                      child: TextField(
                        controller: _dayController,
                        readOnly: true,
                        style: GoogleFonts.mulish(
                          fontSize: 18,
                          color: Theme.of(context).primaryColorDark,
                        ),
                        decoration: InputDecoration(
                          hintText: 'Выберите дату',
                          filled: true,
                          fillColor: Theme.of(context).primaryColorLight,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(15),
                            borderSide: BorderSide.none,
                          ),
                          contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
                          suffixIcon: Icon(Icons.calendar_today, color: Theme.of(context).primaryColorDark),
                        ),
                        onTap: () async {
                          final selectedDate = await showDatePicker(
                            context: context,
                            initialDate: _day ?? DateTime.now(),
                            firstDate: DateTime(2020),
                            lastDate: DateTime(2050),
                          );
                          if (selectedDate != null) {
                            setState(() {
                              _day = selectedDate;
                              _dayController.text = _day!.toIso8601String().substring(0, 10);
                            });
                          }
                        },
                      ),
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Expanded(
                          child: Container(
                            margin: const EdgeInsets.only(right: 10),
                            child: ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                elevation: 0,
                                backgroundColor: Theme.of(context).focusColor,
                                padding: const EdgeInsets.symmetric(vertical: 15),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(15),
                                ),
                              ),
                              onPressed: () {
                                widget.onEdit(
                                    widget.note.id, _titleController.text, _textController.text, _plantId, _day);
                                Navigator.pop(context);
                              },
                              child: Text(
                                'Сохранить',
                                style: GoogleFonts.mulish(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                    color: Theme.of(context).primaryColorDark),
                              ),
                            ),
                          ),
                        ),
                        Expanded(
                          child: Container(
                            margin: const EdgeInsets.only(left: 10),
                            child: ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                elevation: 0,
                                backgroundColor: Theme.of(context).primaryColorLight,
                                padding: const EdgeInsets.symmetric(vertical: 15),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(15),
                                  side: BorderSide(
                                    color: Theme.of(context).primaryColorDark,
                                    width: 2,
                                  ),
                                ),
                              ),
                              onPressed: () => Navigator.pop(context),
                              child: Text(
                                'Отменить',
                                style: GoogleFonts.mulish(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                    color: Theme.of(context).primaryColorDark),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
