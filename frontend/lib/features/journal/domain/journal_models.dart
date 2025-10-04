class JournalEntryModel {
  const JournalEntryModel({
    required this.id,
    required this.content,
    required this.createdAt,
    required this.updatedAt,
    this.title,
    this.mood,
    this.tags = const [],
  });

  final String id;
  final String content;
  final DateTime createdAt;
  final DateTime updatedAt;
  final String? title;
  final String? mood;
  final List<String> tags;

  factory JournalEntryModel.fromJson(Map<String, dynamic> json) {
    return JournalEntryModel(
      id: json['id'] as String? ?? '',
      content: json['content'] as String? ?? '',
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
      title: json['title'] as String?,
      mood: json['mood'] as String?,
      tags: (json['tags'] as List<dynamic>? ?? [])
          .map((tag) => tag as String)
          .toList(),
    );
  }
}

class JournalSummaryModel {
  const JournalSummaryModel(
      {required this.totalEntries, this.moodCounts = const {}});

  final int totalEntries;
  final Map<String, int> moodCounts;

  factory JournalSummaryModel.fromJson(Map<String, dynamic> json) {
    final moodCounts = <String, int>{};
    final raw = json['mood_counts'];
    if (raw is Map<String, dynamic>) {
      for (final entry in raw.entries) {
        moodCounts[entry.key] = (entry.value as num).toInt();
      }
    }
    return JournalSummaryModel(
      totalEntries: (json['total_entries'] as num?)?.toInt() ?? 0,
      moodCounts: moodCounts,
    );
  }
}

class JournalState {
  const JournalState({
    required this.entries,
    this.summary,
    this.isLoading = false,
    this.isSubmitting = false,
    this.errorMessage,
  });

  final List<JournalEntryModel> entries;
  final JournalSummaryModel? summary;
  final bool isLoading;
  final bool isSubmitting;
  final String? errorMessage;

  factory JournalState.initial() {
    return const JournalState(entries: [], isLoading: true);
  }

  JournalState copyWith({
    List<JournalEntryModel>? entries,
    JournalSummaryModel? summary,
    bool? isLoading,
    bool? isSubmitting,
    String? errorMessage,
    bool clearError = false,
  }) {
    return JournalState(
      entries: entries ?? this.entries,
      summary: summary ?? this.summary,
      isLoading: isLoading ?? this.isLoading,
      isSubmitting: isSubmitting ?? this.isSubmitting,
      errorMessage: clearError ? null : errorMessage ?? this.errorMessage,
    );
  }
}
