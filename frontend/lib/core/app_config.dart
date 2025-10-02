class AppConfig {
  const AppConfig({
    this.apiBaseUrl = defaultBaseUrl,
    this.connectTimeout = const Duration(seconds: 10),
    this.receiveTimeout = const Duration(seconds: 20),
  });

  static const String defaultBaseUrl = 'http://localhost:8000/api';

  final String apiBaseUrl;
  final Duration connectTimeout;
  final Duration receiveTimeout;

  AppConfig copyWith({
    String? apiBaseUrl,
    Duration? connectTimeout,
    Duration? receiveTimeout,
  }) {
    return AppConfig(
      apiBaseUrl: apiBaseUrl ?? this.apiBaseUrl,
      connectTimeout: connectTimeout ?? this.connectTimeout,
      receiveTimeout: receiveTimeout ?? this.receiveTimeout,
    );
  }
}
