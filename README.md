#Real-Time Chess Game


#Project Description
This project is a real-time chess game where two players can compete against each other using WebSocket for live updates. The app uses Flask for the web server and Flask-SocketIO for real-time communication.

#Features
Real-Time Gameplay: Two players can play chess against each other in real time.
User Registration and Login: Basic endpoints for user registration and login.
WebSocket Communication: Real-time updates for immediate feedback.
Initial Chess Setup: Standard starting positions for the chessboard.

Basic Game Logic: Handles moves between players, switching turns after each move.

#Assumption:
 The project is for a real-time chess game where two players can play against each other over WebSocket.
 The games and users are stored in dictionaries in memory.
 This approach is suitable for a simple application or for development purposes. For production use, persistent storage would be required.
User Registration and Login
Basic endpoints are used for user registration and login.
 This ensures that users can register and log in, but the authentication process is t simple without secure password handling or session management.
WebSocket Communication
The application uses WebSocket for real-time updates.
 Real-time updates are crucial for providing immediate feedback to players, enhancing the gaming experience.
Initial Chess Setup
 The chess board is initialized with the standard starting positions of a chess game.
Using the standard setup makes the game recognizable and easier for players to start playing immediately.
