<div align="center">

# ✨ Lyra – Your Empathetic Mental Health Companion

*Named after the constellation that guides travelers, Lyra brings light, hope, and clarity during life's emotional challenges.*

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev/)

**Compassionate, AI-powered mental health support—accessible 24/7 through a safe, privacy-first conversational experience.**

[Features](#-key-features) • [Demo](#-screenshots) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## 🌟 Vision

**Normalize seeking mental health support** by offering compassionate, culturally aware, always-available help that **complements—not replaces**—licensed therapy.

### The Problem We're Solving

- 🕐 **Long wait times** and **high costs** limit access to mental healthcare
- 😔 **Stigma** prevents early intervention and open conversations
- ⚠️ **Crisis escalation** can occur when support is unavailable at critical moments
- 🤖 **Generic chatbots** miss nuance and cultural sensitivity, risking harm
- 🔓 Many tools ignore **privacy, safety, and ethical guardrails**

---

## 💡 Key Features

<table>
<tr>
<td width="50%">

### 🗣️ Empathetic Conversations
- **Google Gemini 2.5 Pro** powered responses
- Context-aware emotional support
- Automatic retry with shorter context on token limits
- Graceful fallback for API failures

</td>
<td width="50%">

### 🛡️ Safety-First Design
- **Crisis detection** with localized helplines
- Real-time safety evaluation
- Clear disclaimers throughout
- Never provides harmful instructions

</td>
</tr>
<tr>
<td width="50%">

### 📔 Personal Journaling
- Private, reflective space
- Mood tagging and tracking
- Entry summaries and insights
- Export and backup options

</td>
<td width="50%">

### 📊 Mood Analytics
- Daily mood logging
- Intensity tracking (1-10 scale)
- Trend visualization
- Pattern recognition

</td>
</tr>
<tr>
<td width="50%">

### 🎯 Emotion Detection
- Text-based emotion analysis
- Personalized coping suggestions
- Culturally sensitive responses
- Evidence-based techniques

</td>
<td width="50%">

### 🌍 Multilingual Support
- Locale-aware responses
- Regional crisis resources
- Culturally appropriate guidance
- Timezone considerations

</td>
</tr>
</table>

---

## 🏗️ Architecture

### Tech Stack

#### Backend
```
FastAPI (0.115.0)         → High-performance REST API
Uvicorn                   → ASGI server
Google Gemini 2.5 Pro     → LLM for conversations
Pydantic                  → Data validation
Python 3.13+              → Core language
```

#### Frontend
```
Flutter 3.3+              → Cross-platform UI
Riverpod                  → State management
Dio                       → HTTP client
Material Design 3         → Modern UI components
```

### System Architecture

```
┌─────────────────┐
│  Flutter App    │  ← User Interface (Mobile/Web)
└────────┬────────┘
         │ HTTPS/REST
         ▼
┌─────────────────┐
│   FastAPI       │  ← Backend API Layer
│   Gateway       │
└────────┬────────┘
         │
    ┌────┴─────┬──────────┬──────────┐
    ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Convo   │ │Safety  │ │Emotion │ │Mood    │
│Service │ │Service │ │Service │ │Service │
└───┬────┘ └────────┘ └────────┘ └────────┘
    │
    ▼
┌────────────────┐
│ Google Gemini  │  ← AI Language Model
│   2.5 Pro      │
└────────────────┘
```

### Key Design Patterns

- **Service Layer Architecture**: Separation of concerns with dedicated services
- **Dependency Injection**: Clean, testable code structure
- **Error Recovery**: Automatic retry with exponential backoff
- **Fallback Mechanisms**: Rule-based responses when AI is unavailable

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** (backend)
- **Flutter 3.3+** (frontend)
- **Google Gemini API Key** ([Get one here](https://ai.google.dev/))

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Run the server
uvicorn app.main:app --reload

# API will be available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Get Flutter dependencies
flutter pub get

# Run on Chrome (web)
flutter run -d chrome

# Or run on your connected device
flutter run
```

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v

# Run only passing asyncio tests
pytest tests/ -k asyncio -v
```

---

## 📡 API Endpoints

### Health & Status
```http
GET /api/health
```

### Chat
```http
POST /api/chat/session
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "I'm feeling anxious about tomorrow"}
  ],
  "locale": "en-US"
}
```

### Safety Check
```http
POST /api/safety/check
Content-Type: application/json

{
  "text": "I'm having a hard day",
  "locale": "en-US"
}
```

### Mood Tracking
```http
POST /api/mood/{user_id}/logs
Content-Type: application/json

{
  "mood": "anxious",
  "intensity": 6,
  "notes": "Work deadline approaching"
}
```

### Journal Entries
```http
POST /api/journal/{user_id}/entries
Content-Type: application/json

{
  "title": "Evening Reflection",
  "content": "Today was challenging but I made it through",
  "mood": "hopeful",
  "tags": ["daily", "reflection"]
}
```

---

## 🎨 Screenshots

> **Note**: Add screenshots of your application here

```
[Chat Interface]  [Mood Tracker]  [Journal View]
```

---

## 🔐 Ethics, Privacy & Safety

### Our Commitments

✅ **Not a Substitute for Professional Care**
- Clear disclaimers throughout the app
- Nudges toward professional help when appropriate
- Crisis resources readily available

✅ **Privacy First**
- No unnecessary data collection
- Local storage where possible
- Clear data handling policies

✅ **Safety Protocols**
- Crisis intent detection
- Region-specific emergency resources
- Immediate escalation pathways
- Never provides harmful instructions

✅ **Transparent Operation**
- Open-source codebase
- Clear AI boundaries
- Honest about limitations

### Crisis Resources

- **International**: [findahelpline.com](https://findahelpline.com/)
- **India (Kiran)**: 1800-599-0019
- **US (988)**: 988 Suicide & Crisis Lifeline
- **Emergency**: Always contact local emergency services (911, 112, etc.)

---

## 🧪 Testing

### Test Coverage

```bash
# Run all tests with coverage
pytest tests/ --cov=app --cov-report=html

# Current coverage: Core APIs and services
✅ Health check
✅ Chat session flow
✅ Journal CRUD operations
✅ Mood logging and trends
✅ Safety detection
✅ Gemini response handling
```

### Key Test Files

- `tests/test_api.py` - API integration tests
- `tests/test_conversation_service.py` - Gemini handling tests
- `tests/conftest.py` - Test fixtures and setup

---

## 🛠️ Development

### Project Structure

```
Lyra_Companion/
├── backend/
│   ├── app/
│   │   ├── api/              # API routes
│   │   │   └── routes/       # Endpoint handlers
│   │   ├── core/             # Configuration & events
│   │   ├── models/           # Data models (future DB)
│   │   ├── schemas/          # Pydantic models
│   │   ├── services/         # Business logic
│   │   │   ├── conversation.py  # Gemini integration
│   │   │   ├── emotion.py       # Emotion detection
│   │   │   ├── safety.py        # Crisis detection
│   │   │   ├── mood.py          # Mood tracking
│   │   │   └── journal.py       # Journal management
│   │   └── utils/            # Helper functions
│   ├── tests/                # Test suite
│   ├── docs/                 # Documentation
│   └── requirements.txt      # Python dependencies
│
└── frontend/
    └── lib/
        ├── core/             # App config & providers
        ├── features/         # Feature modules
        ├── models/           # Data models
        ├── screens/          # UI screens
        └── services/         # API clients
```

### Key Files

| File | Purpose |
|------|---------|
| `backend/app/services/conversation.py` | Gemini API integration with retry logic |
| `backend/app/services/safety.py` | Crisis detection and safety evaluation |
| `backend/app/core/config.py` | Environment configuration |
| `frontend/lib/core/providers.dart` | Riverpod state management |

### Recent Improvements

✨ **Enhanced Gemini Error Handling** (Oct 2025)
- Robust response parsing for empty candidates
- Automatic retry with shorter context on `MAX_TOKENS`
- Comprehensive finish_reason logging
- Graceful fallback to rule-based responses

See [GEMINI_FIX_2025_10_04.md](backend/docs/GEMINI_FIX_2025_10_04.md) for technical details.

---

## 🤝 Contributing

We welcome contributions from:
- 🧑‍⚕️ Mental health professionals
- 🎨 UX/UI designers
- 💻 Developers
- 📝 Technical writers
- 🌍 Translators

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- Write tests for new features
- Follow existing code style (Ruff for Python, Dart conventions)
- Update documentation
- Ensure all tests pass
- Add meaningful commit messages

---

## 📚 Documentation

- [API Documentation](http://localhost:8000/docs) - Interactive Swagger docs
- [Gemini Fix Details](backend/docs/GEMINI_FIX_2025_10_04.md) - Error handling improvements
- [Project Cleanup Summary](CLEANUP_SUMMARY.md) - Recent maintenance work

---

## 🎯 Roadmap

### Phase 1: Foundation (Current)
- [x] FastAPI backend with core services
- [x] Flutter mobile/web client
- [x] Google Gemini integration
- [x] Basic mood tracking
- [x] Journal functionality
- [x] Safety detection

### Phase 2: Enhancement (Next)
- [ ] User authentication & profiles
- [ ] Persistent database (MongoDB/PostgreSQL)
- [ ] Advanced emotion analytics
- [ ] Coping exercise library
- [ ] Push notifications for check-ins
- [ ] Offline mode support

### Phase 3: Scale (Future)
- [ ] Multilingual support (5+ languages)
- [ ] Therapist dashboard (with consent)
- [ ] Community features (moderated)
- [ ] Integration with wearables
- [ ] Insurance/healthcare provider partnerships
- [ ] Research & impact studies

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙋 About the Creator

Mental health support is deeply personal to me. I've witnessed friends and peers struggle silently due to stigma and access barriers. **Lyra** is my contribution to making compassionate support feel reachable—anytime, anywhere—while honoring safety, ethics, and human dignity.

If you're working on similar initiatives or want to collaborate, feel free to reach out!

---

## ⚠️ Important Disclaimers

**This application does not provide medical advice.**

Lyra is an **empathetic companion**, not a licensed therapist or medical professional. It is designed to complement—not replace—professional mental health care.

### When to Seek Professional Help

✋ **Seek immediate help if you:**
- Have thoughts of harming yourself or others
- Are experiencing a mental health crisis
- Need diagnosis or treatment
- Require medication management

### Resources

- **Crisis Text Line**: Text HOME to 741741
- **National Suicide Prevention Lifeline**: 1-800-273-8255
- **SAMHSA National Helpline**: 1-800-662-4357
- **Emergency Services**: 911 (US) or your local emergency number

---

<div align="center">

**Built with ❤️ and hope for a world where mental health support is accessible to all**

[⬆ Back to Top](#-lyra--your-empathetic-mental-health-companion)

</div>
