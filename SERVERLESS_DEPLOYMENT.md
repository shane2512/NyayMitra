# NyayMitra Serverless Deployment Guide

## Overview

NyayMitra has been converted to a fully serverless architecture using Vercel Functions. This eliminates the need for a traditional Flask backend and provides automatic scaling, better performance, and reduced operational overhead.

## Architecture Changes

### Before (Traditional Backend)
- Flask server running on port 5000
- Monolithic backend with all agents in one process
- Manual server management and scaling
- Single point of failure

### After (Serverless)
- Individual Vercel Functions for each API endpoint
- Distributed, auto-scaling architecture
- Zero server management
- Built-in redundancy and fault tolerance

## Serverless Functions

The following serverless functions have been created:

### Core Analysis
- `/api/analyze` - Contract analysis with PDF processing
- `/api/health` - Health check endpoint
- `/api/test` - API connectivity testing

### Chat & Conversation
- `/api/chat` - Single message processing
- `/api/chat-batch` - Batch question processing
- `/api/chat-history` - Session history retrieval
- `/api/chat-clear` - Session cleanup

### Voice Features
- `/api/chat-transcribe` - Audio transcription (STT)
- `/api/chat-voice` - Text-to-speech conversion

### Translation & Localization
- `/api/languages` - Supported languages list
- `/api/translator-metrics` - Translation service metrics

### Rate Limiting & Monitoring
- `/api/rate-limit-status` - Current rate limit status
- `/api/rate-limit-reset` - Reset rate limits (debug only)

## Deployment Steps

### 1. Prerequisites
- Vercel account
- Node.js 18+ installed
- Git repository

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
GEMINI_API_KEY=your_actual_api_key
ELEVEN_API_KEY=your_elevenlabs_key
VOICE_ID=your_voice_id
```

### 3. Vercel Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy to Vercel
vercel --prod

# Set environment variables in Vercel dashboard
vercel env add GEMINI_API_KEY
vercel env add ELEVEN_API_KEY
vercel env add VOICE_ID
```

### 4. Frontend Configuration
Update the API base URL in `frontend/src/api.js`:
```javascript
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-vercel-app.vercel.app/api' 
  : 'http://localhost:3000/api';
```

## Key Features Preserved

### ✅ Contract Analysis
- PDF text extraction using PyMuPDF
- AI-powered summarization with Gemini 2.5 Flash
- Risk analysis and recommendations
- Multi-language support (12 languages)

### ✅ AI Chat Assistant
- Context-aware conversations
- Batch question processing
- Session management
- Follow-up suggestions

### ✅ Voice Features
- Audio transcription using ElevenLabs STT
- Text-to-speech synthesis
- Voice chat interface

### ✅ Rate Limiting
- Circuit breaker pattern
- Per-minute and daily limits
- Exponential backoff
- Request statistics

### ✅ Translation Support
- 12 supported languages
- User interest-based summaries
- Cultural appropriateness
- Structured output parsing

## Performance Benefits

### Scalability
- Automatic scaling based on demand
- No cold start issues for frequently used functions
- Global edge deployment

### Reliability
- Built-in redundancy
- Automatic failover
- Zero downtime deployments

### Cost Efficiency
- Pay-per-execution model
- No idle server costs
- Optimized resource usage

## Development Workflow

### Local Development
```bash
# Install dependencies
cd frontend && npm install

# Start development server (includes API proxy)
npm run dev
```

### Testing Serverless Functions Locally
```bash
# Install Vercel CLI
npm install -g vercel

# Run local development server
vercel dev
```

### Deployment
```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

## Configuration Management

### Environment Variables
All configuration is managed through environment variables:
- `GEMINI_API_KEY` - Google Gemini API key
- `GEMINI_MODEL` - AI model version (gemini-2.5-flash)
- `ELEVEN_API_KEY` - ElevenLabs API key for voice features
- `VOICE_ID` - ElevenLabs voice ID
- Rate limiting parameters

### Vercel Configuration
The `vercel.json` file defines:
- Function runtime (Python 3.9)
- Environment variable mapping
- Build configuration
- Function-specific settings

## Monitoring & Debugging

### Vercel Dashboard
- Function execution logs
- Performance metrics
- Error tracking
- Usage analytics

### Rate Limiting Monitoring
- Real-time status via `/api/rate-limit-status`
- Circuit breaker status
- Request statistics
- Warning thresholds

## Migration Benefits

### For Users
- Faster response times (global CDN)
- Better reliability (99.99% uptime)
- Improved scalability
- No maintenance windows

### For Developers
- Simplified deployment process
- Automatic scaling
- Built-in monitoring
- Zero server management

### For Operations
- Reduced infrastructure costs
- Automatic security updates
- Built-in backup and recovery
- Global availability

## Troubleshooting

### Common Issues
1. **Cold Start Delays**: First request may be slower
2. **File Upload Limits**: Vercel has 4.5MB limit for serverless functions
3. **Timeout Limits**: Functions timeout after 10 seconds (hobby) or 60 seconds (pro)

### Solutions
1. Use function warming for critical endpoints
2. Implement file chunking for large uploads
3. Optimize function execution time
4. Use appropriate Vercel plan for requirements

## Next Steps

1. **Monitor Performance**: Use Vercel analytics to track function performance
2. **Optimize Cold Starts**: Implement function warming if needed
3. **Scale Resources**: Upgrade Vercel plan based on usage
4. **Add Monitoring**: Integrate with external monitoring tools
5. **Implement Caching**: Add Redis or similar for session storage

## Support

For issues or questions:
1. Check Vercel function logs
2. Review rate limiting status
3. Verify environment variables
4. Test individual endpoints
5. Contact development team

The serverless architecture provides a robust, scalable foundation for NyayMitra while maintaining all existing functionality and improving performance characteristics.
