enum ChatRole { user, assistant, system }

ChatRole chatRoleFromString(String value) {
  switch (value) {
    case 'assistant':
      return ChatRole.assistant;
    case 'system':
      return ChatRole.system;
    case 'user':
    default:
      return ChatRole.user;
  }
}

String chatRoleToString(ChatRole role) {
  switch (role) {
    case ChatRole.assistant:
      return 'assistant';
    case ChatRole.system:
      return 'system';
    case ChatRole.user:
      return 'user';
  }
}

class ChatMessageModel {
  const ChatMessageModel({required this.role, required this.content});

  final ChatRole role;
  final String content;

  factory ChatMessageModel.fromJson(Map<String, dynamic> json) {
    return ChatMessageModel(
      role: chatRoleFromString(json['role'] as String? ?? 'assistant'),
      content: json['content'] as String? ?? '',
    );
  }

  factory ChatMessageModel.user(String content) {
    return ChatMessageModel(role: ChatRole.user, content: content);
  }

  factory ChatMessageModel.assistant(String content) {
    return ChatMessageModel(role: ChatRole.assistant, content: content);
  }

  Map<String, dynamic> toJson() {
    return {
      'role': chatRoleToString(role),
      'content': content,
    };
  }

  bool get isUser => role == ChatRole.user;

  bool get isAssistant => role == ChatRole.assistant;
}

class CopingSuggestionModel {
  const CopingSuggestionModel({
    required this.title,
    required this.description,
    this.resourceUrl,
  });

  final String title;
  final String description;
  final String? resourceUrl;

  factory CopingSuggestionModel.fromJson(Map<String, dynamic> json) {
    return CopingSuggestionModel(
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      resourceUrl: json['resource_url'] as String?,
    );
  }
}

class EmotionEstimateModel {
  const EmotionEstimateModel({required this.label, required this.confidence});

  final String label;
  final double confidence;

  factory EmotionEstimateModel.fromJson(Map<String, dynamic> json) {
    return EmotionEstimateModel(
      label: json['label'] as String? ?? '',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0,
    );
  }
}

class SafetyCheckResultModel {
  const SafetyCheckResultModel({
    required this.crisisDetected,
    this.riskLevel,
    this.matchedCategory,
    this.recommendedActions = const [],
    this.hotline,
  });

  final bool crisisDetected;
  final String? riskLevel;
  final String? matchedCategory;
  final List<String> recommendedActions;
  final String? hotline;

  factory SafetyCheckResultModel.fromJson(Map<String, dynamic> json) {
    return SafetyCheckResultModel(
      crisisDetected: json['crisis_detected'] as bool? ?? false,
      riskLevel: json['risk_level'] as String?,
      matchedCategory: json['matched_category'] as String?,
      recommendedActions: (json['recommended_actions'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          const [],
      hotline: json['hotline'] as String?,
    );
  }
}

class ChatState {
  const ChatState({
    required this.messages,
    required this.suggestions,
    required this.emotions,
    this.safety,
    this.isLoading = false,
    this.errorMessage,
  });

  final List<ChatMessageModel> messages;
  final List<CopingSuggestionModel> suggestions;
  final List<EmotionEstimateModel> emotions;
  final SafetyCheckResultModel? safety;
  final bool isLoading;
  final String? errorMessage;

  factory ChatState.initial() {
    return ChatState(
      messages: const [
        ChatMessageModel(
          role: ChatRole.assistant,
          content:
              'Hi, I am Lyra. I am here to hold space for whatever you are feeling. What would you like to share today?',
        ),
      ],
      suggestions: const [],
      emotions: const [],
    );
  }

  ChatState copyWith({
    List<ChatMessageModel>? messages,
    List<CopingSuggestionModel>? suggestions,
    List<EmotionEstimateModel>? emotions,
    SafetyCheckResultModel? safety,
    bool? isLoading,
    String? errorMessage,
    bool clearError = false,
  }) {
    return ChatState(
      messages: messages ?? this.messages,
      suggestions: suggestions ?? this.suggestions,
      emotions: emotions ?? this.emotions,
      safety: safety ?? this.safety,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: clearError ? null : errorMessage ?? this.errorMessage,
    );
  }
}
