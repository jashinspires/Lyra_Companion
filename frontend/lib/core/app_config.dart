class AppConfig {
  const AppConfig({
    this.apiBaseUrl = defaultBaseUrl,
    this.connectTimeout = const Duration(seconds: 10),
    this.receiveTimeout = const Duration(seconds: 20),
    this.defaultUserId = 'demo-user',
  });

  static const String defaultBaseUrl = 'http://localhost:8000/api';

  final String apiBaseUrl;
  final Duration connectTimeout;
  final Duration receiveTimeout;
  final String defaultUserId;

  AppConfig copyWith({
    String? apiBaseUrl,
    Duration? connectTimeout,
    Duration? receiveTimeout,
    String? defaultUserId,
  }) {
    return AppConfig(
      apiBaseUrl: apiBaseUrl ?? this.apiBaseUrl,
      connectTimeout: connectTimeout ?? this.connectTimeout,
      receiveTimeout: receiveTimeout ?? this.receiveTimeout,
      defaultUserId: defaultUserId ?? this.defaultUserId,
    );
  }
}
