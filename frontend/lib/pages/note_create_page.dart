import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/note.dart';
import '../models/user.dart';
import '../pages/home_page.dart';
import '../pages/notes_page.dart';
import '../services/auth_service.dart';
import '../services/note_service.dart';
import '../services/user_service.dart';
import '../services/plant_service.dart';
import '../models/plant.dart';

class NoteCreatePage extends StatefulWidget {
  NoteCreatePage({super.key});

  @override
  _NoteCreatePageState createState() => _NoteCreatePageState();
}

class _NoteCreatePageState extends State<NoteCreatePage> {
  late AuthService _authService;
  late NoteService _noteService;
  late UserService _userService;
  late PlantService _plantService;
  late User _user;
  List<Plant> _plants = [];
  String _error = '';
  bool _isLoading = false;
  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _textController = TextEditingController();
  int? _plantId;
  DateTime? _day;

  @override
  void initState() {
    super.initState();
    _initServices();
  }

  Future<void> _initServices() async {
    try {
      _authService = await AuthService.create();
      _noteService = NoteService(_authService);
      _userService = UserService(_authService);
      _plantService = PlantService(_authService);
      _user = await _userService.getUser();
      _plants = await _plantService.getPlants();
    } catch (e) {
      setState(() {
        _error = e.toString();
      });
    }
  }

  void _updatePlantId(int? value) {
    setState(() {
      _plantId = value;
    });
  }

  void _updateDay(DateTime? value) {
    setState(() {
      _day = value;
    });
  }

  Future<void> _createNote() async {
    if (_titleController.text.isEmpty) {
      setState(() {
        _error = 'Введите заголовок';
      });
      _clearError();
      return;
    }

    if (_textController.text.isEmpty) {
      setState(() {
        _error = 'Введите текст';
      });
      _clearError();
      return;
    }

    if (_plantId == null && _day == null) {
      setState(() {
        _error = 'Выберите растение или дату';
      });
      _clearError();
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      final note = Note(
        id: 0,
        userId: _user.id,
        title: _titleController.text,
        text: _textController.text,
        plantId: _plantId,
        day: _day,
      );

      await _noteService.createNote(note);

      if (mounted) {
        Navigator.pushAndRemoveUntil(
          context,
          PageRouteBuilder(
            pageBuilder: (context, animation, secondaryAnimation) => const NotesPage(),
            transitionDuration: Duration.zero,
          ),
          (route) => false,
        );
      }
    } catch (e) {
      setState(() {
        _error = e.toString();
      });
      _clearError();
    } finally {
      setState(() {
        _isLoading = false;
      });
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(toolbarHeight: 40),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Expanded(
            flex: 2,
            child: NoteCreateAppBar(),
          ),
          Container(
            decoration: BoxDecoration(
              color: Theme.of(context).primaryColorDark,
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(50),
                topRight: Radius.circular(50),
              ),
              border: Border(
                top: BorderSide(color: Theme.of(context).primaryColorLight),
              ),
            ),
            padding: const EdgeInsets.symmetric(horizontal: 10),
            child: NoteCreateForm(
              createNote: _createNote,
              isLoading: _isLoading,
              error: _error,
              titleController: _titleController,
              textController: _textController,
              updatePlantId: _updatePlantId,
              updateDay: _updateDay,
              plants: _plants,
            ),
          ),
        ],
      ),
    );
  }
}

class NoteCreateAppBar extends StatelessWidget {
  const NoteCreateAppBar({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 30, right: 30, top: 30, bottom: 0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Flora\nFriend',
            style: GoogleFonts.museoModerno(fontSize: 80, fontWeight: FontWeight.bold, height: 1),
          ),
          IconButton(
              onPressed: () {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (context) => const NotesPage()),
                );
              },
              icon: Icon(
                Icons.book_outlined,
                color: Theme.of(context).primaryColorDark,
                size: 50,
              )),
          IconButton(
              onPressed: () {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (context) => const HomePage()),
                );
              },
              icon: Icon(
                Icons.home_outlined,
                color: Theme.of(context).primaryColorDark,
                size: 50,
              )),
        ],
      ),
    );
  }
}

class NoteCreateForm extends StatefulWidget {
  final void Function() createNote;
  final TextEditingController titleController;
  final TextEditingController textController;
  final void Function(int?) updatePlantId;
  final void Function(DateTime?) updateDay;
  final bool isLoading;
  final String error;
  final List<Plant> plants;

  NoteCreateForm(
      {required this.createNote,
      required this.isLoading,
      required this.error,
      required this.titleController,
      required this.textController,
      required this.updatePlantId,
      required this.updateDay,
      required this.plants});

  @override
  _NoteCreateFormState createState() => _NoteCreateFormState();
}

class _NoteCreateFormState extends State<NoteCreateForm> {
  final TextEditingController _dayController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.only(left: 10, right: 10, top: 40, bottom: 30),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Создание заметки',
                  style: GoogleFonts.mulish(
                      fontSize: 35,
                      fontWeight: FontWeight.w100,
                      color: Theme.of(context).primaryColorLight,
                      height: 1)),
            ],
          ),
        ),
        Container(
          decoration: BoxDecoration(
            color: Theme.of(context).primaryColorLight,
            borderRadius: BorderRadius.circular(30),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          margin: const EdgeInsets.symmetric(vertical: 10),
          child: TextField(
            style: GoogleFonts.mulish(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Theme.of(context).primaryColorDark,
            ),
            controller: widget.titleController,
            decoration: InputDecoration(
              hintText: 'введите заголовок...',
              hintStyle: GoogleFonts.mulish(
                fontSize: 20,
                fontWeight: FontWeight.w100,
                color: Colors.grey,
              ),
              prefixIcon: Icon(Icons.title_outlined),
              border: InputBorder.none,
            ),
          ),
        ),
        Container(
          decoration: BoxDecoration(
            color: Theme.of(context).primaryColorLight,
            borderRadius: BorderRadius.circular(30),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          margin: const EdgeInsets.symmetric(vertical: 10),
          child: TextField(
            minLines: 4,
            maxLines: 4,
            style: GoogleFonts.mulish(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Theme.of(context).primaryColorDark,
            ),
            controller: widget.textController,
            decoration: InputDecoration(
              hintText: 'введите текст...',
              hintStyle: GoogleFonts.mulish(
                fontSize: 20,
                fontWeight: FontWeight.w100,
                color: Colors.grey,
              ),
              prefixIcon: Icon(Icons.description_outlined),
              border: InputBorder.none,
            ),
          ),
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: Theme.of(context).primaryColorLight,
                  borderRadius: BorderRadius.circular(30),
                ),
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                margin: const EdgeInsets.symmetric(vertical: 10),
                child: DropdownButtonFormField<int>(
                  dropdownColor: Theme.of(context).primaryColorLight,
                  items:
                      widget.plants.map((plant) => DropdownMenuItem(value: plant.id, child: Text(plant.name))).toList(),
                  onChanged: (value) {
                    widget.updatePlantId(value?.toInt());
                  },
                  style: GoogleFonts.mulish(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).primaryColorDark,
                  ),
                  decoration: InputDecoration(
                    hintText: 'растение...',
                    hintStyle: GoogleFonts.mulish(
                      fontSize: 20,
                      fontWeight: FontWeight.w100,
                      color: Colors.grey,
                    ),
                    prefixIcon: Icon(Icons.local_florist_outlined),
                    border: InputBorder.none,
                  ),
                ),
              ),
            ),
            SizedBox(width: 10),
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: Theme.of(context).primaryColorLight,
                  borderRadius: BorderRadius.circular(30),
                ),
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                margin: const EdgeInsets.symmetric(vertical: 10),
                child: TextField(
                  controller: _dayController,
                  readOnly: true,
                  style: GoogleFonts.mulish(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).primaryColorDark,
                  ),
                  decoration: InputDecoration(
                    hintText: 'день...',
                    hintStyle: GoogleFonts.mulish(
                      fontSize: 20,
                      fontWeight: FontWeight.w100,
                      color: Colors.grey,
                    ),
                    prefixIcon: Icon(Icons.calendar_today),
                    border: InputBorder.none,
                  ),
                  onTap: () async {
                    DateTime? pickedDate = await showDatePicker(
                      context: context,
                      initialDate: DateTime.now(),
                      firstDate: DateTime(2024),
                      lastDate: DateTime(2026),
                      locale: const Locale('ru', 'RU'),
                      builder: (context, child) {
                        return Theme(
                          data: Theme.of(context).copyWith(
                            colorScheme: ColorScheme.light(
                              primary: Theme.of(context).primaryColorDark,
                              onPrimary: Theme.of(context).primaryColorLight,
                              surface: Theme.of(context).focusColor,
                              onSurface: Theme.of(context).primaryColorDark,
                            ),
                          ),
                          child: child!,
                        );
                      },
                    );
                    if (pickedDate != null) {
                      _dayController.text = pickedDate.toIso8601String().substring(0, 10);
                      widget.updateDay(pickedDate);
                    }
                  },
                ),
              ),
            ),
          ],
        ),
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 10),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Theme.of(context).focusColor,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30),
                        side: BorderSide(color: Theme.of(context).primaryColorDark),
                      ),
                    ),
                    onPressed: widget.createNote,
                    child: Padding(
                      padding: const EdgeInsets.symmetric(vertical: 15),
                      child: Text('Далее',
                          style: GoogleFonts.mulish(
                              fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorDark)),
                    )),
              ),
            ],
          ),
        ),
        if (widget.error != 'null')
          Text(widget.error,
              style: GoogleFonts.mulish(
                  fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorLight)),
      ],
    );
  }
}
