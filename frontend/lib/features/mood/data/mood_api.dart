import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/providers.dart';

class MoodApi {
  const MoodApi(this._dio);

  final Dio _dio;

  Future<Response<dynamic>> listLogs(String userId) {
    return _dio.get('/mood/$userId/logs');
  }

  Future<Response<dynamic>> createLog(
      String userId, Map<String, dynamic> payload) {
    return _dio.post('/mood/$userId/logs', data: payload);
  }

  Future<Response<dynamic>> trend(String userId) {
    return _dio.get('/mood/$userId/trend');
  }
}

final moodApiProvider = Provider<MoodApi>((ref) {
  final dio = ref.watch(dioProvider);
  return MoodApi(dio);
});
