import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart';
import '../pages/general/bottom_navigator.dart';
import '../models/note.dart';
import '../services/auth_service.dart';
import '../pages/home_page.dart';

class CalendarPage extends StatefulWidget {
  const CalendarPage({super.key});

  @override
  State<CalendarPage> createState() => _CalendarPageState();
}

class _CalendarPageState extends State<CalendarPage> {
  DateTime _focusedDay = DateTime.now();
  DateTime? _selectedDay;

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
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
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
                      'Календарь',
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
              flex: 7,
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: 0.0, vertical: 0.0),
                child: TableCalendar(
                  locale: 'ru_RU',
                  focusedDay: _focusedDay, // День, на котором фокусируется календарь
                  firstDay: DateTime(2020), // Первый доступный день
                  lastDay: DateTime(2030), // Последний доступный день
                  startingDayOfWeek: StartingDayOfWeek.monday,
                  selectedDayPredicate: (day) => isSameDay(_selectedDay, day), // Проверка выбранного дня
                  onDaySelected: (selectedDay, focusedDay) {
                    setState(() {
                      _selectedDay = selectedDay; // Обновляем выбранный день
                      _focusedDay = focusedDay; // Обновляем фокусированный день
                    });
                  },
                  onFormatChanged: (format) {
                    setState(() {}); // Перерисовываем виджет при изменении формата
                  },
                  onPageChanged: (focusedDay) {
                    _focusedDay = focusedDay; // Обновляем фокусированный день при листании
                  },
                  calendarFormat: CalendarFormat.month,
                  rowHeight: 40,
                  daysOfWeekHeight: 30,
                  headerStyle: HeaderStyle(
                    formatButtonVisible: false,
                    titleCentered: true,
                    headerPadding: EdgeInsets.fromLTRB(0.0, 5.0, 0.0, 7.0),
                    titleTextStyle: TextStyle(fontSize: 25, fontFamily: 'Mulish', fontWeight: FontWeight.normal),
                  ),
                  daysOfWeekStyle: DaysOfWeekStyle(
                    weekdayStyle: TextStyle(color: Colors.black),
                    weekendStyle: TextStyle(color: Colors.red),
                  ),
                  calendarStyle: CalendarStyle(
                    isTodayHighlighted: true, // Подсвечивать сегодняшний день
                    selectedDecoration: BoxDecoration(
                      color: Theme.of(context).highlightColor, // Цвет выделения выбранного дня
                      shape: BoxShape.rectangle,
                    ),
                    todayDecoration: BoxDecoration(
                      color: Theme.of(context).primaryColor, // Цвет выделения сегодняшнего дня
                      shape: BoxShape.rectangle,
                    ),
                    defaultDecoration: BoxDecoration(
                      shape: BoxShape.circle, // Форма обычных дней
                    ),
                    weekendDecoration: BoxDecoration(
                      shape: BoxShape.circle, // Форма выходных дней
                    ),
                  ),
                ),
              ),
            ),
            Expanded(
              flex: 6,
              child: Container(
                decoration: BoxDecoration(
                  color: Theme.of(context).cardColor,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: NotesWindow(
                  selectedDate: _selectedDay ?? _focusedDay,
                  onDateChanged: (newDate) {
                    setState(() {
                      _selectedDay = newDate;
                      _focusedDay = newDate;
                    });
                  },
                ),
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigator(),
    );
  }
}

class NotesWindow extends StatefulWidget {
  final DateTime selectedDate;
  final Function(DateTime) onDateChanged;

  const NotesWindow({
    super.key,
    required this.selectedDate,
    required this.onDateChanged,
  });

  @override
  State<NotesWindow> createState() => _NotesWindowState();
}

class _NotesWindowState extends State<NotesWindow> {
  late AuthService _authService;
  List<Note> notes = [];
  bool isLoading = false;
  String? error;

  @override
  void initState() {
    super.initState();
    _initServices();
  }

  Future<void> _initServices() async {
    _authService = await AuthService.create();
    _loadNotes();
  }

  @override
  void didUpdateWidget(NotesWindow oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.selectedDate != widget.selectedDate) {
      _loadNotes();
    }
  }

  Future<void> _loadNotes() async {
    setState(() {
      isLoading = true;
      error = null;
    });

    try {
      // Имитация загрузки данных
      await Future.delayed(Duration(milliseconds: 800));

      // Демо-данные заметок для выбранной даты
      final demoNotes = _getDemoNotes(widget.selectedDate);

      setState(() {
        notes = demoNotes;
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        error = 'Не удалось загрузить заметки';
        isLoading = false;
      });
    }
  }

  List<Note> _getDemoNotes(DateTime date) {
    // Создаем разные заметки для разных дат
    final day = date.day;

    if (day % 3 == 0) {
      return [
        Note(id: 1, title: 'Полить растения', text: 'Полить растения', day: date, userId: 1, plantId: 1),
        Note(
            id: 2,
            title: 'Проверить влажность почвы',
            text: 'Проверить влажность почвы',
            day: date,
            userId: 1,
            plantId: 1),
      ];
    } else if (day % 3 == 1) {
      return [
        Note(id: 3, title: 'Подкормить растения', text: 'Подкормить растения', day: date, userId: 1, plantId: 1),
      ];
    } else {
      return [];
    }
  }

  void _addNote() {
    showDialog(
      useRootNavigator: false,
      context: context,
      barrierDismissible: true,
      builder: (BuildContext context) {
        String noteText = '';
        return SingleChildScrollView(
          child: AlertDialog(
            backgroundColor: Theme.of(context).primaryColorLight,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(20),
            ),
            insetPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 200),
            title: Text(
              'Новая заметка',
              style: TextStyle(
                color: Theme.of(context).cardColor,
                fontFamily: 'Mulish',
                fontSize: 25,
              ),
            ),
            content: Container(
              decoration: BoxDecoration(
                color: Theme.of(context).primaryColor,
                borderRadius: BorderRadius.circular(15),
              ),
              width: MediaQuery.of(context).size.width,
              child: TextField(
                autofocus: true,
                maxLines: 3,
                decoration: InputDecoration(
                  hintText: 'Введите текст заметки...',
                  hintStyle: TextStyle(
                    color: Theme.of(context).cardColor.withAlpha(100),
                    fontFamily: 'Mulish',
                  ),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(15),
                    borderSide: BorderSide(
                      color: Theme.of(context).cardColor,
                    ),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(15),
                    borderSide: BorderSide(
                      color: Theme.of(context).cardColor,
                    ),
                  ),
                ),
                style: TextStyle(
                  color: Theme.of(context).cardColor,
                  fontFamily: 'Mulish',
                ),
                onChanged: (value) {
                  noteText = value;
                },
              ),
            ),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: Text(
                  'Отмена',
                  style: TextStyle(
                    color: Theme.of(context).cardColor,
                    fontFamily: 'Mulish',
                  ),
                ),
              ),
              TextButton(
                onPressed: () async {
                  if (noteText.isNotEmpty) {
                    try {
                      // Имитация создания заметки
                      await Future.delayed(Duration(milliseconds: 500));

                      // Добавляем заметку локально
                      setState(() {
                        notes.add(Note(
                          id: DateTime.now().millisecondsSinceEpoch,
                          title: noteText,
                          text: noteText,
                          day: widget.selectedDate,
                          userId: 1,
                          plantId: 1,
                        ));
                      });

                      Navigator.of(context).pop();
                    } catch (e) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Ошибка при создании заметки'),
                          backgroundColor: Colors.red,
                        ),
                      );
                    }
                  }
                },
                child: Text(
                  'Добавить',
                  style: TextStyle(
                    color: Theme.of(context).cardColor,
                    fontFamily: 'Mulish',
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.fromLTRB(16.0, 10.0, 16.0, 5.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        mainAxisAlignment: MainAxisAlignment.start,
        spacing: 10.0,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                'Уход на ${widget.selectedDate.day < 10 ? "0" : ""}${widget.selectedDate.day}.${widget.selectedDate.month < 10 ? "0" : ""}${widget.selectedDate.month}:',
                style: TextStyle(
                  fontSize: 25.0,
                  fontFamily: 'Mulish',
                  letterSpacing: 5.0,
                  fontWeight: FontWeight.normal,
                  color: Theme.of(context).primaryColorLight,
                ),
              ),
              IconButton(
                onPressed: _addNote,
                icon: Icon(
                  Icons.add_circle_outline,
                  color: Theme.of(context).primaryColorLight,
                  size: 30,
                ),
              ),
            ],
          ),
          Expanded(
            child: isLoading
                ? Center(child: CircularProgressIndicator())
                : error != null
                    ? Center(child: Text(error!))
                    : notes.isEmpty
                        ? Center(child: Text('Нет заметок на этот день'))
                        : ListView.builder(
                            padding: EdgeInsets.only(top: 10.0),
                            itemCount: notes.length,
                            itemBuilder: (context, index) {
                              final note = notes[index];
                              return Container(
                                margin: EdgeInsets.only(bottom: 5.0),
                                decoration: BoxDecoration(
                                  color: Theme.of(context).primaryColorLight,
                                  borderRadius: BorderRadius.circular(20),
                                ),
                                child: ListTile(
                                  title: Text(
                                    "- ${note.text}",
                                    style: TextStyle(
                                      color: Theme.of(context).cardColor,
                                      fontFamily: 'Mulish',
                                    ),
                                  ),
                                ),
                              );
                            },
                          ),
          ),
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 60.0),
            child: ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                backgroundColor: Theme.of(context).highlightColor,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
              ),
              child: Text(
                'Посмотреть все',
                style: TextStyle(color: Theme.of(context).cardColor),
              ),
            ),
          )
        ],
      ),
    );
  }
}
