import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/models.dart';
import '../models/task.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000';
  
  final http.Client _client = http.Client();

  // Tasks
  Future<Task> createTask({
    required String goal,
    required AgenticPattern pattern,
    List<Message> messages = const [],
    Map<String, dynamic> config = const {},
  }) async {
    final response = await _client.post(
      Uri.parse('$baseUrl/tasks'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'goal': goal,
        'pattern': _patternToString(pattern),
        'messages': messages.map((m) => m.toJson()).toList(),
        'config': config,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to create task: ${response.body}');
    }

    final data = jsonDecode(response.body);
    return await getTask(data['task_id']);
  }

  Future<Task> getTask(String taskId) async {
    final response = await _client.get(Uri.parse('$baseUrl/tasks/$taskId'));

    if (response.statusCode != 200) {
      throw Exception('Failed to get task: ${response.body}');
    }

    final data = jsonDecode(response.body);
    return Task.fromJson(data);
  }

  // Agents
  Future<List<Agent>> getAgents() async {
    final response = await _client.get(Uri.parse('$baseUrl/agents'));

    if (response.statusCode != 200) {
      throw Exception('Failed to get agents: ${response.body}');
    }

    final data = jsonDecode(response.body) as List;
    return data.map((json) => Agent.fromJson(json)).toList();
  }

  Future<Agent> createAgent({
    required String name,
    required String role,
    required String systemPrompt,
    List<String> tools = const [],
  }) async {
    final response = await _client.post(
      Uri.parse('$baseUrl/agents'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': name,
        'role': role,
        'system_prompt': systemPrompt,
        'tools': tools,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to create agent: ${response.body}');
    }

    final data = jsonDecode(response.body);
    return Agent.fromJson(data);
  }

  // Tools
  Future<List<Tool>> getTools() async {
    final response = await _client.get(Uri.parse('$baseUrl/tools'));

    if (response.statusCode != 200) {
      throw Exception('Failed to get tools: ${response.body}');
    }

    final data = jsonDecode(response.body) as List;
    return data.map((json) => Tool.fromJson(json)).toList();
  }

  Future<void> registerTool(Tool tool) async {
    final response = await _client.post(
      Uri.parse('$baseUrl/tools/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(tool.toJson()),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to register tool: ${response.body}');
    }
  }

  String _patternToString(AgenticPattern pattern) {
    switch (pattern) {
      case AgenticPattern.reflection:
        return 'reflection';
      case AgenticPattern.toolUse:
        return 'tool_use';
      case AgenticPattern.react:
        return 'react';
      case AgenticPattern.planning:
        return 'planning';
      case AgenticPattern.multiAgent:
        return 'multi_agent';
    }
  }

  void dispose() {
    _client.close();
  }
}
