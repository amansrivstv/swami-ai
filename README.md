# Swami AI

A RAG (Retrieval-Augmented Generation) based AI chatbot designed to behave like a wise swami (spiritual teacher). The application combines vector search capabilities with large language models to provide contextually aware, philosophical responses.

## 🚀 Features

- **AI-Powered Chat**: Uses TogetherAI's Llama-3.3-70B-Instruct-Turbo-Free model for intelligent responses
- **Vector Search**: Leverages Weaviate vector database for semantic search and context retrieval
- **Real-time Communication**: WebSocket support for live chat with HTTP fallback
- **Cross-platform Frontend**: Flutter-based UI that works on web, mobile, and desktop
- **Context-Aware Responses**: Retrieves relevant knowledge base content to enhance AI responses
- **Docker Support**: Complete containerized setup for easy deployment

## 🏗️ Architecture

The project consists of three main components:

### Backend (FastAPI)
- **FastAPI** server with WebSocket support
- **Weaviate** vector database for semantic search
- **TogetherAI** integration for LLM responses
- **RESTful API** endpoints for chat functionality

### Frontend (Flutter)
- **Cross-platform** Flutter application
- **Real-time chat** interface with WebSocket support
- **Material Design** UI components
- **Connection management** with status indicators

### Infrastructure
- **Docker Compose** for orchestration
- **Weaviate** vector database container
- **Nginx** for frontend serving (in production)


## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd swami-ai
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
# TogetherAI API Key (get from https://together.ai)
TOGETHER_API_KEY=your_together_api_key_here
```

### 3. Data Preparation

The application requires pre-processed data files in the `backend/app/static/` directory:
- `chunks.txt` - Text chunks from your knowledge base
- `vectors.txt` - Vector embeddings for semantic search

### 4. Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Weaviate**: http://localhost:8080

## 🔧 Manual Setup (Development)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export TOGETHER_API_KEY=your_api_key_here

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install Flutter dependencies
flutter pub get

# Run the application
flutter run -d chrome  # For web
flutter run             # For connected device
```

### Weaviate Setup

```bash
# Run Weaviate with Docker
docker run -d \
  --name weaviate \
  -p 8080:8080 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
  -e ENABLE_API_BASED_MODULES=true \
  -e CLUSTER_HOSTNAME='node1' \
  cr.weaviate.io/semitechnologies/weaviate:1.32.4
```

## 📚 API Documentation

### Chat Endpoints

- `POST /api/v1/chat/send` - Send message and get AI response
- `GET /api/v1/chat/history/{session_id}` - Get chat history
- `DELETE /api/v1/chat/clear/{session_id}` - Clear chat history
- `WebSocket /api/v1/chat/ws/{session_id}` - Real-time chat

### Health Check

- `GET /health` - Service health status
- `GET /weaviate/status` - Weaviate connection status

## 🎯 Usage

### Starting a Chat Session

1. Open the application in your browser at http://localhost:3000
2. Click "Start Chat" to begin a new session
3. Type your philosophical or spiritual questions
4. Receive contextually aware responses from the AI swami

### Example Conversations

- Ask about life's purpose and meaning
- Discuss spiritual practices and meditation
- Explore philosophical concepts
- Seek guidance on personal growth

## 🔍 Troubleshooting

### Common Issues

1. **Connection Failed**
   - Ensure all Docker containers are running
   - Check if ports 3000, 8000, and 8080 are available
   - Verify TOGETHER_API_KEY is set correctly

2. **Weaviate Connection Issues**
   - Check Weaviate container logs: `docker-compose logs weaviate`
   - Ensure data files exist in `backend/app/static/`
   - Verify Weaviate is accessible at http://localhost:8080

3. **AI Responses Not Working**
   - Verify TogetherAI API key is valid
   - Check backend logs for API errors
   - Ensure sufficient API credits on TogetherAI

4. **Frontend Not Loading**
   - Check if Flutter dependencies are installed
   - Verify backend is running on port 8000
   - Check browser console for errors

### Debug Commands

```bash
# Check container status
docker-compose ps

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs weaviate

# Restart specific service
docker-compose restart backend

# Rebuild containers
docker-compose build --no-cache
```

## 🛡️ Security Considerations

- Configure `ALLOWED_ORIGINS` in production
- Use environment variables for sensitive data
- Implement proper authentication for production use
- Secure Weaviate with authentication
- Use HTTPS in production

## 📈 Performance Optimization

- Monitor Weaviate query performance
- Optimize vector search parameters
- Implement response caching
- Use connection pooling for database
- Monitor TogetherAI API usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **TogetherAI** for providing the LLM API
- **Weaviate** for vector database capabilities
- **FastAPI** for the robust backend framework
- **Flutter** for cross-platform development

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review the logs for error details
- Open an issue on the repository
