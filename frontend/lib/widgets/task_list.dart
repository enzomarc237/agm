import 'package:flutter/material.dart';
import '../models/models.dart';
import '../models/task.dart';

class TaskList extends StatelessWidget {
  final List<Task> tasks;

  const TaskList({super.key, required this.tasks});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: tasks.length,
      itemBuilder: (context, index) {
        final task = tasks[index];
        return TaskListItem(task: task);
      },
    );
  }
}

class TaskListItem extends StatelessWidget {
  final Task task;

  const TaskListItem({super.key, required this.task});

  @override
  Widget build(BuildContext context) {
    final pattern = _getPatternFromString(task.pattern);
    
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      child: ListTile(
        leading: Icon(
          pattern?.icon ?? Icons.help_outline,
          color: pattern?.color ?? Colors.grey,
        ),
        title: Text(
          task.goal,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        subtitle: Row(
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
              decoration: BoxDecoration(
                color: _getStatusColor(task.status).withOpacity(0.1),
                borderRadius: BorderRadius.circular(4),
              ),
              child: Text(
                task.status.toUpperCase(),
                style: TextStyle(
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                  color: _getStatusColor(task.status),
                ),
              ),
            ),
            const SizedBox(width: 8),
            Text(
              pattern?.displayName ?? task.pattern,
              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
            ),
          ],
        ),
        trailing: Text(
          _getTimeAgo(task.createdAt),
          style: TextStyle(fontSize: 12, color: Colors.grey[500]),
        ),
        isThreeLine: false,
        onTap: () => _showTaskDetail(context),
      ),
    );
  }

  void _showTaskDetail(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.7,
        minChildSize: 0.5,
        maxChildSize: 0.95,
        expand: false,
        builder: (context, scrollController) {
          return TaskDetailView(task: task, scrollController: scrollController);
        },
      ),
    );
  }

  AgenticPattern? _getPatternFromString(String patternStr) {
    switch (patternStr.toLowerCase()) {
      case 'reflection':
        return AgenticPattern.reflection;
      case 'tool_use':
        return AgenticPattern.toolUse;
      case 'react':
        return AgenticPattern.react;
      case 'planning':
        return AgenticPattern.planning;
      case 'multi_agent':
        return AgenticPattern.multiAgent;
      default:
        return null;
    }
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'pending':
        return Colors.grey;
      case 'running':
        return Colors.blue;
      case 'completed':
        return Colors.green;
      case 'failed':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  String _getTimeAgo(DateTime dateTime) {
    final difference = DateTime.now().difference(dateTime);
    
    if (difference.inDays > 0) {
      return '${difference.inDays}d ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours}h ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes}m ago';
    } else {
      return 'Just now';
    }
  }
}

class TaskDetailView extends StatelessWidget {
  final Task task;
  final ScrollController scrollController;

  const TaskDetailView({
    super.key,
    required this.task,
    required this.scrollController,
  });

  @override
  Widget build(BuildContext context) {
    final pattern = _getPatternFromString(task.pattern);
    
    return Padding(
      padding: const EdgeInsets.all(16),
      child: ListView(
        controller: scrollController,
        children: [
          Row(
            children: [
              Icon(
                pattern?.icon ?? Icons.help_outline,
                size: 32,
                color: pattern?.color ?? Colors.grey,
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      task.goal,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Task ID: ${task.id}',
                      style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                    ),
                  ],
                ),
              ),
              Chip(
                label: Text(task.status.toUpperCase()),
                backgroundColor: _getStatusColor(task.status).withOpacity(0.1),
              ),
            ],
          ),
          const Divider(height: 32),
          if (task.plan != null && task.plan!.isNotEmpty) ...[
            const Text(
              'Plan',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            ...task.plan!.asMap().entries.map((entry) {
              return Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CircleAvatar(
                      radius: 12,
                      backgroundColor: pattern?.color ?? Colors.blue,
                      child: Text(
                        '${entry.key + 1}',
                        style: const TextStyle(
                          fontSize: 12,
                          color: Colors.white,
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(entry.value),
                    ),
                  ],
                ),
              );
            }),
            const Divider(height: 32),
          ],
          if (task.reflection != null) ...[
            const Text(
              'Reflection',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.purple.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.purple.withOpacity(0.3)),
              ),
              child: Text(task.reflection!),
            ),
            const Divider(height: 32),
          ],
          const Text(
            'Logs',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          ...task.logs.map((log) {
            return Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.grey[100],
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(
                          log['type'] ?? 'info',
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const Spacer(),
                        Text(
                          _formatTimestamp(log['timestamp']),
                          style: TextStyle(fontSize: 10, color: Colors.grey[600]),
                        ),
                      ],
                    ),
                    if (log['message'] != null) ...[
                      const SizedBox(height: 4),
                      Text(log['message']),
                    ],
                  ],
                ),
              ),
            );
          }),
        ],
      ),
    );
  }

  AgenticPattern? _getPatternFromString(String patternStr) {
    switch (patternStr.toLowerCase()) {
      case 'reflection':
        return AgenticPattern.reflection;
      case 'tool_use':
        return AgenticPattern.toolUse;
      case 'react':
        return AgenticPattern.react;
      case 'planning':
        return AgenticPattern.planning;
      case 'multi_agent':
        return AgenticPattern.multiAgent;
      default:
        return null;
    }
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'pending':
        return Colors.grey;
      case 'running':
        return Colors.blue;
      case 'completed':
        return Colors.green;
      case 'failed':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  String _formatTimestamp(String? timestamp) {
    if (timestamp == null) return '';
    try {
      final dateTime = DateTime.parse(timestamp);
      return '${dateTime.hour}:${dateTime.minute.toString().padLeft(2, '0')}';
    } catch (e) {
      return '';
    }
  }
}
