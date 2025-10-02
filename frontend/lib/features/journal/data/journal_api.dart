import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/providers.dart';

class JournalApi {
  const JournalApi(this._dio);

  final Dio _dio;

  Future<Response<dynamic>> listEntries(String userId) {
    return _dio.get('/journal/$userId/entries');
  }

  Future<Response<dynamic>> createEntry(
      String userId, Map<String, dynamic> payload) {
    return _dio.post('/journal/$userId/entries', data: payload);
  }

  Future<Response<dynamic>> summary(String userId) {
    return _dio.get('/journal/$userId/summary');
  }
}

final journalApiProvider = Provider<JournalApi>((ref) {
  final dio = ref.watch(dioProvider);
  return JournalApi(dio);
});
