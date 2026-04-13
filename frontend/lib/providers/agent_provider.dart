import 'package:flutter/foundation.dart';
import '../models/task.dart';
import '../services/api_service.dart';

class AgentProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  List<Agent> _agents = [];
  bool _isLoading = false;
  String? _error;

  List<Agent> get agents => _agents;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> loadAgents() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _agents = await _apiService.getAgents();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> createAgent({
    required String name,
    required String role,
    required String systemPrompt,
    List<String> tools = const [],
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final agent = await _apiService.createAgent(
        name: name,
        role: role,
        systemPrompt: systemPrompt,
        tools: tools,
      );
      
      _agents.add(agent);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void removeAgent(String agentId) {
    _agents.removeWhere((agent) => agent.id == agentId);
    notifyListeners();
  }

  @override
  void dispose() {
    _apiService.dispose();
    super.dispose();
  }
}
