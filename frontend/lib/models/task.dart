class Task {
  final String id;
  final String goal;
  final String pattern;
  final String status;
  final String? result;
  final List<dynamic> logs;
  final List<String>? plan;
  final String? reflection;
  final DateTime createdAt;

  Task({
    required this.id,
    required this.goal,
    required this.pattern,
    required this.status,
    this.result,
    this.logs = const [],
    this.plan,
    this.reflection,
    required this.createdAt,
  });

  factory Task.fromJson(Map<String, dynamic> json) => Task(
        id: json['task_id'],
        goal: json['goal'] ?? '',
        pattern: json['pattern'] ?? '',
        status: json['status'] ?? 'pending',
        result: json['result'],
        logs: json['logs'] ?? [],
        plan: json['plan'] != null 
            ? List<String>.from(json['plan']) 
            : null,
        reflection: json['reflection'],
        createdAt: json['created_at'] != null 
            ? DateTime.parse(json['created_at']) 
            : DateTime.now(),
      );

  Map<String, dynamic> toJson() => {
        'task_id': id,
        'goal': goal,
        'pattern': pattern,
        'status': status,
        'result': result,
        'logs': logs,
        'plan': plan,
        'reflection': reflection,
        'created_at': createdAt.toIso8601String(),
      };

  bool get isCompleted => status == 'completed';
  bool get isRunning => status == 'running';
  bool get isFailed => status == 'failed';
}

class Agent {
  final String id;
  final String name;
  final String role;
  final String systemPrompt;
  final List<String> tools;

  Agent({
    required this.id,
    required this.name,
    required this.role,
    required this.systemPrompt,
    this.tools = const [],
  });

  factory Agent.fromJson(Map<String, dynamic> json) => Agent(
        id: json['agent_id'] ?? '',
        name: json['name'] ?? '',
        role: json['role'] ?? '',
        systemPrompt: json['system_prompt'] ?? '',
        tools: json['tools'] != null 
            ? List<String>.from(json['tools']) 
            : [],
      );

  Map<String, dynamic> toJson() => {
        'agent_id': id,
        'name': name,
        'role': role,
        'system_prompt': systemPrompt,
        'tools': tools,
      };
}

class Tool {
  final String name;
  final String description;
  final Map<String, dynamic> parameters;

  Tool({
    required this.name,
    required this.description,
    required this.parameters,
  });

  factory Tool.fromJson(Map<String, dynamic> json) => Tool(
        name: json['name'] ?? '',
        description: json['description'] ?? '',
        parameters: json['parameters'] ?? {},
      );

  Map<String, dynamic> toJson() => {
        'name': name,
        'description': description,
        'parameters': parameters,
      };
}
