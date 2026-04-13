import 'package:flutter/material.dart';

enum AgenticPattern {
  reflection('Reflection', 'Self-correction and refinement'),
  toolUse('Tool Use', 'External data and action integration'),
  react('ReAct', 'Reasoning + Acting iterative loop'),
  planning('Planning', 'Multi-step task management'),
  multiAgent('Multi-Agent', 'Collaborative problem solving');

  final String displayName;
  final String description;

  const AgenticPattern(this.displayName, this.description);

  IconData get icon {
    switch (this) {
      case AgenticPattern.reflection:
        return Icons.self_improvement;
      case AgenticPattern.toolUse:
        return Icons.build;
      case AgenticPattern.react:
        return Icons.loop;
      case AgenticPattern.planning:
        return Icons.list_alt;
      case AgenticPattern.multiAgent:
        return Icons.people;
    }
  }

  Color get color {
    switch (this) {
      case AgenticPattern.reflection:
        return Colors.purple;
      case AgenticPattern.toolUse:
        return Colors.blue;
      case AgenticPattern.react:
        return Colors.orange;
      case AgenticPattern.planning:
        return Colors.green;
      case AgenticPattern.multiAgent:
        return Colors.teal;
    }
  }
}

enum TaskStatus {
  pending('Pending'),
  running('Running'),
  completed('Completed'),
  failed('Failed');

  final String displayName;

  const TaskStatus(this.displayName);

  Color get color {
    switch (this) {
      case TaskStatus.pending:
        return Colors.grey;
      case TaskStatus.running:
        return Colors.blue;
      case TaskStatus.completed:
        return Colors.green;
      case TaskStatus.failed:
        return Colors.red;
    }
  }

  IconData get icon {
    switch (this) {
      case TaskStatus.pending:
        return Icons.schedule;
      case TaskStatus.running:
        return Icons.hourglass_empty;
      case TaskStatus.completed:
        return Icons.check_circle;
      case TaskStatus.failed:
        return Icons.error;
    }
  }
}

class Message {
  final String role;
  final String content;

  Message({required this.role, required this.content});

  Map<String, dynamic> toJson() => {
        'role': role,
        'content': content,
      };

  factory Message.fromJson(Map<String, dynamic> json) => Message(
        role: json['role'],
        content: json['content'],
      );
}

class LogEntry {
  final String type;
  final String message;
  final String timestamp;
  final dynamic content;

  LogEntry({
    required this.type,
    required this.message,
    required this.timestamp,
    this.content,
  });

  factory LogEntry.fromJson(Map<String, dynamic> json) => LogEntry(
        type: json['type'] ?? '',
        message: json['message'] ?? '',
        timestamp: json['timestamp'] ?? '',
        content: json['content'],
      );
}
