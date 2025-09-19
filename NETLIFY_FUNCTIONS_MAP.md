# NyayMitra Netlify Functions Mapping

## 🚀 **Netlify Functions Overview**

All Vercel-specific files have been removed. The application now uses 4 consolidated Netlify Functions:

### **1. Contract Analysis Function**
- **File**: `netlify/functions/analyze.py`
- **Endpoint**: `/.netlify/functions/analyze`
- **Frontend API**: `analyzeContract()`
- **Functionality**: PDF contract analysis with translation support

### **2. Chat Functions (Consolidated)**
- **File**: `netlify/functions/chat.py`
- **Base Endpoint**: `/.netlify/functions/chat`
- **Sub-functions** (via `?action=` parameter):
  - `?action=chat` → Single chat message
  - `?action=batch` → Batch chat processing  
  - `?action=history` → Chat history retrieval
  - `?action=clear` → Clear chat session
  - `?action=voice` → Text-to-speech (ElevenLabs)
  - `?action=transcribe` → Audio transcription (placeholder)

**Frontend API Mappings:**
- `sendChatMessage()` → `chat?action=chat`
- `sendBatchChatMessage()` → `chat?action=batch`
- `getChatHistory()` → `chat?action=history`
- `clearChatSession()` → `chat?action=clear`
- `sendVoiceMessage()` → `chat?action=voice`
- `transcribeAudio()` → `chat?action=transcribe`

### **3. Admin Functions (Consolidated)**
- **File**: `netlify/functions/admin.py`
- **Base Endpoint**: `/.netlify/functions/admin`
- **Sub-functions** (via `?action=` parameter):
  - `?action=health` → Health check (default)
  - `?action=test` → Configuration test
  - `?action=rate-limit-status` → Rate limiting status
  - `?action=rate-limit-reset` → Reset rate limits (debug only)
  - `?action=translator-metrics` → Translation metrics

**Frontend API Mappings:**
- `healthCheck()` → `admin?action=health`
- `getRateLimitStatus()` → `admin?action=rate-limit-status`
- `getTranslatorMetrics()` → `admin?action=translator-metrics`

### **4. Languages Function**
- **File**: `netlify/functions/languages.py`
- **Endpoint**: `/.netlify/functions/languages`
- **Frontend API**: `getSupportedLanguages()`
- **Functionality**: Returns supported languages for translation

## 🔧 **Supporting Files**

### **Agents Directory**: `netlify/functions/agents/`
- `conversation_agent.py` - AI chat functionality
- `moderator.py` - Contract analysis orchestration
- `rate_limiter.py` - Rate limiting with circuit breaker
- `risk_analyzer.py` - Risk assessment
- `summarizer.py` - Contract summaries
- `translator.py` - Multi-language translation

### **Configuration Files**:
- `config.py` - Environment configuration
- `utils.py` - Shared utilities and response formatting
- `requirements.txt` - Python dependencies (NO OpenAI!)

## 📋 **Dependencies (Clean)**
```
google-generativeai==0.3.2  # Gemini AI
pypdf2==3.0.1              # PDF processing (lightweight)
python-dotenv==0.19.2       # Environment variables
elevenlabs==0.2.27          # Voice synthesis only
```

## 🎯 **Voice Functionality Status**
- ✅ **Text-to-Speech**: Full ElevenLabs integration
- ✅ **Speech-to-Text**: Placeholder (ready for any STT service)
- ❌ **No OpenAI dependency** - completely removed

## 🌐 **Frontend API Configuration**
```javascript
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/.netlify/functions' 
  : 'http://localhost:8888/.netlify/functions';
```

## 📁 **Removed Vercel Files**
- ❌ `vercel.json` - Removed
- ❌ `api/` directory - Removed  
- ❌ `.vercelignore` - Removed
- ❌ `runtime.txt` - Removed
- ❌ All Vercel-specific configurations - Removed

## ✅ **All Functions Verified**
- [x] Contract analysis working
- [x] Chat functionality complete
- [x] Voice synthesis ready
- [x] Admin endpoints functional
- [x] Language support available
- [x] Rate limiting implemented
- [x] Translation features ready
- [x] Frontend API mappings correct

**Status: Ready for Netlify deployment! 🚀**
