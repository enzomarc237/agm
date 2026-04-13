import 'package:flutter/foundation.dart';
import '../models/models.dart';
import '../models/task.dart';
import '../services/api_service.dart';

class TaskProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  List<Task> _tasks = [];
  Task? _currentTask;
  bool _isLoading = false;
  String? _error;

  List<Task> get tasks => _tasks;
  Task? get currentTask => _currentTask;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> createTask({
    required String goal,
    required AgenticPattern pattern,
    List<Message> messages = const [],
    Map<String, dynamic> config = const {},
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final task = await _apiService.createTask(
        goal: goal,
        pattern: pattern,
        messages: messages,
        config: config,
      );
      
      _tasks.insert(0, task);
      _currentTask = task;
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> refreshTask(String taskId) async {
    try {
      final task = await _apiService.getTask(taskId);
      
      final index = _tasks.indexWhere((t) => t.id == taskId);
      if (index != -1) {
        _tasks[index] = task;
      }
      
      if (_currentTask?.id == taskId) {
        _currentTask = task;
      }
      
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }

  void selectTask(Task task) {
    _currentTask = task;
    notifyListeners();
  }

  void clearCurrentTask() {
    _currentTask = null;
    notifyListeners();
  }

  @override
  void dispose() {
    _apiService.dispose();
    super.dispose();
  }
}
