import 'package:flutter/material.dart';
import '../models/models.dart';

class PatternSelector extends StatelessWidget {
  final AgenticPattern? selectedPattern;
  final ValueChanged<AgenticPattern?> onChanged;

  const PatternSelector({
    super.key,
    this.selectedPattern,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Select Pattern',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: AgenticPattern.values.map((pattern) {
            final isSelected = selectedPattern == pattern;
            return ChoiceChip(
              label: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(pattern.icon, size: 16, color: pattern.color),
                  const SizedBox(width: 4),
                  Text(pattern.displayName),
                ],
              ),
              selected: isSelected,
              onSelected: (selected) {
                if (selected) {
                  onChanged(pattern);
                }
              },
              selectedColor: pattern.color.withOpacity(0.2),
              labelStyle: TextStyle(
                color: isSelected ? pattern.color : null,
                fontWeight: isSelected ? FontWeight.bold : null,
              ),
            );
          }).toList(),
        ),
        if (selectedPattern != null) ...[
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: selectedPattern!.color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Row(
              children: [
                Icon(Icons.info_outline, color: selectedPattern!.color),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    selectedPattern!.description,
                    style: TextStyle(color: selectedPattern!.color),
                  ),
                ),
              ],
            ),
          ),
        ],
      ],
    );
  }
}
