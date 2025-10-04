import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/providers.dart';
import '../data/journal_api.dart';
import '../domain/journal_models.dart';

final journalControllerProvider =
    StateNotifierProvider<JournalController, JournalState>((ref) {
  final api = ref.watch(journalApiProvider);
  final userId = ref.watch(userIdProvider);
  return JournalController(api, userId);
});

class JournalController extends StateNotifier<JournalState> {
  JournalController(this._api, this._userId) : super(JournalState.initial()) {
    loadEntries();
  }

  final JournalApi _api;
  final String _userId;

  Future<void> loadEntries() async {
    state = state.copyWith(isLoading: true, clearError: true);
    try {
      final responses = await Future.wait([
        _api.listEntries(_userId),
        _api.summary(_userId),
      ]);
      final entries = (responses[0].data as List<dynamic>)
          .map((item) =>
              JournalEntryModel.fromJson(item as Map<String, dynamic>))
          .toList()
        ..sort((a, b) => b.createdAt.compareTo(a.createdAt));
      final summary = JournalSummaryModel.fromJson(
        responses[1].data as Map<String, dynamic>,
      );
      state = state.copyWith(
        entries: entries,
        summary: summary,
        isLoading: false,
      );
    } on DioException catch (error) {
      final detail = error.response?.data is Map<String, dynamic>
          ? (error.response?.data['detail'] as String? ?? '')
          : '';
      _handleFailure(detail.isEmpty ? null : detail);
    } catch (_) {
      _handleFailure(null);
    }
  }

  Future<bool> createEntry({
    required String content,
    String? title,
    String? mood,
    List<String> tags = const [],
  }) async {
    final payload = <String, dynamic>{
      'content': content,
      if (title != null && title.trim().isNotEmpty) 'title': title.trim(),
      if (mood != null && mood.trim().isNotEmpty) 'mood': mood.trim(),
      if (tags.isNotEmpty) 'tags': tags,
    };

    state = state.copyWith(isSubmitting: true, clearError: true);
    try {
      final response = await _api.createEntry(_userId, payload);
      final created =
          JournalEntryModel.fromJson(response.data as Map<String, dynamic>);
      final updatedEntries = [created, ...state.entries];
      state = state.copyWith(
        entries: updatedEntries,
        isSubmitting: false,
      );
      return true;
    } on DioException catch (error) {
      final detail = error.response?.data is Map<String, dynamic>
          ? (error.response?.data['detail'] as String? ?? '')
          : '';
      _handleFailure(detail.isEmpty ? null : detail);
    } catch (_) {
      _handleFailure(null);
    }
    state = state.copyWith(isSubmitting: false);
    return false;
  }

  void _handleFailure(String? detail) {
    final message = detail?.isNotEmpty == true
        ? 'Unable to load journal entries. $detail'
        : 'Unable to load journal entries. Please try again.';
    state = state.copyWith(
      isLoading: false,
      errorMessage: message,
      isSubmitting: false,
    );
  }
}
