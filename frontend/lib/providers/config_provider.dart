import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ConfigProvider extends ChangeNotifier {
  String _llmProvider = 'openai';
  String? _apiKey;
  String _apiBaseUrl = 'http://localhost:8000';
  bool _darkMode = false;
  bool _autoReflection = true;
  int _maxIterations = 10;

  String get llmProvider => _llmProvider;
  String? get apiKey => _apiKey;
  String get apiBaseUrl => _apiBaseUrl;
  bool get darkMode => _darkMode;
  bool get autoReflection => _autoReflection;
  int get maxIterations => _maxIterations;

  Future<void> loadConfig() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      _llmProvider = prefs.getString('llm_provider') ?? 'openai';
      _apiKey = prefs.getString('api_key');
      _apiBaseUrl = prefs.getString('api_base_url') ?? 'http://localhost:8000';
      _darkMode = prefs.getBool('dark_mode') ?? false;
      _autoReflection = prefs.getBool('auto_reflection') ?? true;
      _maxIterations = prefs.getInt('max_iterations') ?? 10;
      notifyListeners();
    } catch (e) {
      debugPrint('Error loading config: $e');
    }
  }

  Future<void> setLlmProvider(String provider) async {
    _llmProvider = provider;
    await _saveString('llm_provider', provider);
    notifyListeners();
  }

  Future<void> setApiKey(String? key) async {
    _apiKey = key;
    if (key != null) {
      await _saveString('api_key', key);
    } else {
      await _remove('api_key');
    }
    notifyListeners();
  }

  Future<void> setApiBaseUrl(String url) async {
    _apiBaseUrl = url;
    await _saveString('api_base_url', url);
    notifyListeners();
  }

  Future<void> setDarkMode(bool enabled) async {
    _darkMode = enabled;
    await _saveBool('dark_mode', enabled);
    notifyListeners();
  }

  Future<void> setAutoReflection(bool enabled) async {
    _autoReflection = enabled;
    await _saveBool('auto_reflection', enabled);
    notifyListeners();
  }

  Future<void> setMaxIterations(int max) async {
    _maxIterations = max;
    await _saveInt('max_iterations', max);
    notifyListeners();
  }

  Future<void> _saveString(String key, String value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(key, value);
  }

  Future<void> _saveBool(String key, bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(key, value);
  }

  Future<void> _saveInt(String key, int value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(key, value);
  }

  Future<void> _remove(String key) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(key);
  }
}
