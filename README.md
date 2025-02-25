# Claude Service API

A Flask-based backend service for AI integration using Anthropic's Claude, with enhanced error handling and system monitoring.

## Configuration

### Environment Variables

The service requires the following environment variables to be set:

1. **API Keys**:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `SESSION_SECRET`: Flask session secret key

2. **Content Variables**:
   The service uses chunked environment variables for large content to stay within environment variable size limits:
   - `RAG_KNOWLEDGE_CONTENT_1` through `RAG_KNOWLEDGE_CONTENT_9`: Chunks of knowledge base content
   - `PROMPT_INSTRUCTIONS`: Claude's instruction set

### Setting Up Environment Variables

1. **Using the Content Splitter Utility**:
   ```bash
   python utils/set_env_chunks.py
   ```
   This will:
   - Split the content into appropriate chunks
   - Set environment variables for development
   - Show previews of content chunks

2. **Manual Setup**:
   If you need to set up the environment variables manually:
   - Use the content splitter to see required chunks: `python utils/content_splitter.py`
   - Set each environment variable according to the output

## Development

### Branches

- `main`: Production-ready code
- `feature/secure-content`: Implementation of environment-based sensitive content

### Switching Branches

To switch back to the main branch:
```bash
git checkout main
git stash  # If you have uncommitted changes
```

## API Endpoints

- `GET /`: Redirects to status dashboard
- `GET /start`: Initialize new conversation thread
- `POST /chat`: Send messages to Claude
- `POST /webhook`: Legacy webhook endpoint
- `GET /status`: View system status dashboard
- `GET /health`: Health check endpoint

## Security

- Sensitive content is stored in environment variables
- API keys and secrets are never committed to the repository
- Content is split into chunks to accommodate environment variable size limits
