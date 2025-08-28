# Frontend Setup for TogetherAI Integration

This document explains how to set up and use the Flutter frontend with the new TogetherAI backend integration.

## Overview

The frontend has been updated to work seamlessly with the new TogetherAI backend that provides:
- **LLM-powered responses** using Llama-3.3-70B-Instruct-Turbo-Free
- **Vector search** using TogetherAI embeddings
- **Real-time chat** via WebSocket and HTTP fallback
- **Context-aware responses** from Weaviate knowledge base

## Setup

### 1. Prerequisites

- Flutter SDK (latest stable version)
- Dart SDK
- Android Studio / VS Code with Flutter extensions

### 2. Install Dependencies

```bash
cd frontend
flutter pub get
```

### 3. Configuration

The frontend is configured to connect to the backend at `http://localhost:8000`. If your backend is running on a different URL, update the constants in `lib/core/constants/app_constants.dart`:

```dart
class AppConstants {
  static const String baseUrl = 'http://localhost:8000';  // Update this
  static const String wsUrl = 'ws://localhost:8000';      // Update this
  // ...
}
```

## Features

### 1. Chat Interface

- **Real-time messaging** with typing indicators
- **Message history** persistence
- **Error handling** with user-friendly messages
- **Loading states** during AI processing

### 2. Connection Management

- **WebSocket support** for real-time communication
- **HTTP fallback** when WebSocket is unavailable
- **Connection status indicator** in the app bar
- **Manual WebSocket toggle** for testing

### 3. UI Components

- **Message bubbles** with different styles for user and AI
- **Typing indicator** with animated dots
- **Chat input** with send button and character limit
- **App bar** with connection status and controls

## Usage

### Starting the App

1. **Run the backend server** (see backend documentation)
2. **Start the Flutter app**:
   ```bash
   cd frontend
   flutter run
   ```

### Testing the Connection

1. **Launch the app**
2. **Tap "Test Connection"** on the home screen
3. **Click "Test Connection"** to verify backend connectivity
4. **Check the results** for any issues

### Using the Chat

1. **Tap "Start Chat"** on the home screen
2. **Type your message** in the input field
3. **Send the message** using the send button or Enter key
4. **Wait for the AI response** (typing indicator will show)
5. **View the conversation** in the message list

## API Integration

### Endpoints Used

- `POST /api/v1/chat/send` - Send message and get AI response
- `GET /api/v1/chat/history/{session_id}` - Get chat history
- `DELETE /api/v1/chat/clear/{session_id}` - Clear chat history
- `WebSocket /api/v1/chat/ws/{session_id}` - Real-time chat

### Data Models

The frontend uses the following data models:

```dart
class ChatMessage {
  final String id;
  final String message;
  final String timestamp;
  final bool isUser;
}
```

## Error Handling

The frontend includes comprehensive error handling:

- **Network errors** - Shows user-friendly error messages
- **API errors** - Displays specific error details
- **WebSocket failures** - Automatically falls back to HTTP
- **Invalid responses** - Handles malformed JSON gracefully

## Development

### Project Structure

```
lib/
├── app/
│   └── app.dart                 # Main app configuration
├── core/
│   ├── constants/
│   │   └── app_constants.dart   # API URLs and settings
│   ├── models/
│   │   └── chat_message.dart    # Data models
│   ├── services/
│   │   ├── api_service.dart     # HTTP API calls
│   │   └── websocket_service.dart # WebSocket communication
│   └── theme/
│       └── app_theme.dart       # App theming
└── features/
    └── chat/
        └── presentation/
            ├── controllers/
            │   └── chat_controller.dart # Chat state management
            ├── pages/
            │   └── chat_page.dart      # Main chat page
            └── widgets/
                ├── chat_app_bar.dart   # App bar with controls
                ├── chat_input.dart     # Message input
                ├── connection_test.dart # Connection testing
                ├── message_bubble.dart # Individual messages
                ├── message_list.dart   # Message list
                └── typing_indicator.dart # Loading animation
```

### Key Components

#### ChatController
- Manages chat state and messages
- Handles WebSocket and HTTP communication
- Provides loading states and error handling

#### ApiService
- Handles HTTP API calls to the backend
- Manages request/response formatting
- Provides error handling and retry logic

#### WebSocketService
- Manages real-time WebSocket communication
- Handles connection state and reconnection
- Provides message streaming

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Ensure backend server is running
   - Check API URLs in `app_constants.dart`
   - Verify network connectivity

2. **WebSocket Not Working**
   - Check if WebSocket endpoint is accessible
   - Verify CORS settings on backend
   - Try HTTP fallback mode

3. **Messages Not Sending**
   - Check backend logs for errors
   - Verify TOGETHER_API_KEY is set
   - Ensure Weaviate is running

4. **Slow Responses**
   - Check TogetherAI API status
   - Verify Weaviate performance
   - Monitor network latency

### Debug Mode

Enable debug logging by running:
```bash
flutter run --debug
```

## Performance

- **Message caching** for better performance
- **Lazy loading** of chat history
- **Optimized UI** with minimal rebuilds
- **Efficient state management** with ChangeNotifier

## Future Enhancements

Potential improvements:
- **Message streaming** for real-time response display
- **File upload** support for documents
- **Voice input** integration
- **Offline mode** with local caching
- **Push notifications** for new messages
- **Multi-language** support
