import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/models.dart';
import '../providers/task_provider.dart';

class NewTaskDialog extends StatefulWidget {
  const NewTaskDialog({super.key});

  @override
  State<NewTaskDialog> createState() => _NewTaskDialogState();
}

class _NewTaskDialogState extends State<NewTaskDialog> {
  final _formKey = GlobalKey<FormState>();
  final _goalController = TextEditingController();
  
  AgenticPattern? _selectedPattern;
  String _patternError = '';

  @override
  void dispose() {
    _goalController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Row(
        children: [
          Icon(Icons.add_task),
          SizedBox(width: 8),
          Text('New Task'),
        ],
      ),
      content: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Goal Input
              TextFormField(
                controller: _goalController,
                decoration: const InputDecoration(
                  labelText: 'Goal',
                  hintText: 'What do you want to accomplish?',
                  prefixIcon: Icon(Icons.target),
                  border: OutlineInputBorder(),
                ),
                maxLines: 3,
                textCapitalization: TextCapitalization.sentences,
                validator: (value) {
                  if (value == null || value.trim().isEmpty) {
                    return 'Please enter a goal';
                  }
                  return null;
                },
              ),
              
              const SizedBox(height: 24),
              
              // Pattern Selection
              Text(
                'Select Agentic Pattern',
                style: Theme.of(context).textTheme.titleSmall,
              ),
              const SizedBox(height: 12),
              
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: AgenticPattern.values.map((pattern) {
                  final isSelected = _selectedPattern == pattern;
                  return ChoiceChip(
                    avatar: Icon(pattern.icon, size: 18, color: pattern.color),
                    label: Text(pattern.displayName),
                    selected: isSelected,
                    onSelected: (selected) {
                      setState(() {
                        _selectedPattern = selected ? pattern : null;
                        _patternError = '';
                      });
                    },
                    selectedColor: pattern.color.withOpacity(0.2),
                    labelStyle: TextStyle(
                      color: isSelected ? pattern.color : null,
                      fontWeight: isSelected ? FontWeight.bold : null,
                    ),
                  );
                }).toList(),
              ),
              
              if (_patternError.isNotEmpty) ...[
                const SizedBox(height: 8),
                Text(
                  _patternError,
                  style: TextStyle(color: Colors.red[700], fontSize: 12),
                ),
              ],
              
              const SizedBox(height: 8),
              
              // Pattern Description
              if (_selectedPattern != null)
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: _selectedPattern!.color.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(
                      color: _selectedPattern!.color.withOpacity(0.3),
                    ),
                  ),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Icon(
                        Icons.info_outline,
                        color: _selectedPattern!.color,
                        size: 20,
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          _selectedPattern!.description,
                          style: TextStyle(
                            fontSize: 13,
                            color: _selectedPattern!.color,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Cancel'),
        ),
        FilledButton.icon(
          onPressed: _submitTask,
          icon: Consumer<TaskProvider>(
            builder: (context, taskProvider, child) {
              if (taskProvider.isLoading) {
                return const SizedBox(
                  width: 16,
                  height: 16,
                  child: CircularProgressIndicator(strokeWidth: 2),
                );
              }
              return const Icon(Icons.send);
            },
          ),
          label: const Text('Create Task'),
        ),
      ],
    );
  }

  void _submitTask() async {
    // Validate form
    if (!_formKey.currentState!.validate()) {
      return;
    }
    
    // Validate pattern selection
    if (_selectedPattern == null) {
      setState(() {
        _patternError = 'Please select an agentic pattern';
      });
      return;
    }
    
    // Create task
    final taskProvider = Provider.of<TaskProvider>(context, listen: false);
    
    try {
      await taskProvider.createTask(
        goal: _goalController.text.trim(),
        pattern: _selectedPattern!,
      );
      
      if (mounted) {
        Navigator.of(context).pop();
        
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Task created successfully!'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error creating task: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }
}
