import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/chat_api.dart';
import '../domain/chat_models.dart';

final chatControllerProvider =
    StateNotifierProvider<ChatController, ChatState>((ref) {
  final api = ref.watch(chatApiProvider);
  return ChatController(api);
});

class ChatController extends StateNotifier<ChatState> {
  ChatController(this._api) : super(ChatState.initial());

  final ChatApi _api;

  Future<void> sendMessage(String text) async {
    final trimmed = text.trim();
    if (trimmed.isEmpty) {
      return;
    }

    final userMessage = ChatMessageModel.user(trimmed);
    final updatedMessages = [...state.messages, userMessage];
    state = state.copyWith(
      messages: updatedMessages,
      isLoading: true,
      clearError: true,
    );

    try {
      final payload = {
        'messages': updatedMessages.map((message) => message.toJson()).toList(),
      };

      final response = await _api.sendMessage(payload);
      final data = response.data as Map<String, dynamic>? ??
          <String, dynamic>{
            'reply': {'role': 'assistant', 'content': ''}
          };

      final replyJson = data['reply'] as Map<String, dynamic>?;
      if (replyJson != null) {
        final assistantMessage = ChatMessageModel.fromJson(replyJson);
        final suggestions = (data['suggestions'] as List<dynamic>? ?? [])
            .map((item) =>
                CopingSuggestionModel.fromJson(item as Map<String, dynamic>))
            .toList();
        final emotions = (data['emotions'] as List<dynamic>? ?? [])
            .map((item) =>
                EmotionEstimateModel.fromJson(item as Map<String, dynamic>))
            .toList();
        final safetyJson = data['safety'] as Map<String, dynamic>?;
        final safety = safetyJson != null
            ? SafetyCheckResultModel.fromJson(safetyJson)
            : null;

        state = state.copyWith(
          messages: [...state.messages, assistantMessage],
          suggestions: suggestions,
          emotions: emotions,
          safety: safety,
          isLoading: false,
        );
      } else {
        _handleFailure();
      }
    } on DioException catch (error) {
      final detail = error.response?.data is Map<String, dynamic>
          ? (error.response?.data['detail'] as String? ?? '')
          : '';
      _handleFailure(additionalMessage: detail);
    } catch (_) {
      _handleFailure();
    }
  }

  void resetError() {
    if (state.errorMessage != null) {
      state = state.copyWith(clearError: true);
    }
  }

  void _handleFailure({String additionalMessage = ''}) {
    final message = additionalMessage.isNotEmpty
        ? 'Unable to send message. $additionalMessage'
        : 'Unable to send message. Please try again.';
    state = state.copyWith(
      isLoading: false,
      errorMessage: message,
    );
  }
}
