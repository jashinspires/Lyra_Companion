import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app_config.dart';

final appConfigProvider = Provider<AppConfig>((ref) {
  return const AppConfig();
});

final dioProvider = Provider<Dio>((ref) {
  final config = ref.watch(appConfigProvider);
  return Dio(
    BaseOptions(
      baseUrl: config.apiBaseUrl,
      connectTimeout: config.connectTimeout,
      receiveTimeout: config.receiveTimeout,
      headers: const {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ),
  );
});
