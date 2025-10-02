import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/providers.dart';

class ChatApi {
  const ChatApi(this._dio);

  final Dio _dio;

  Future<Response<dynamic>> sendMessage(Map<String, dynamic> payload) {
    return _dio.post('/chat/session', data: payload);
  }
}

final chatApiProvider = Provider<ChatApi>((ref) {
  final dio = ref.watch(dioProvider);
  return ChatApi(dio);
});
