from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room
import uuid
import psutil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # Setting  a secret key for session management
socketio = SocketIO(app, cors_allowed_origins="*") 
games = {}
users = {}

class Game:
    def __init__(self, player1, player2):
        self.id = str(uuid.uuid4())  
        self.board = self.create_board() 
        self.players = {player1: 'white', player2: 'black'}  
        self.turn = 'white'  
        self.moves = [] 

    def create_board(self):
      
        return [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]

    def make_move(self, move):
       
        src, dest = move['src'], move['dest']
        piece = self.board[src[0]][src[1]]
        self.board[src[0]][src[1]] = ""
        self.board[dest[0]][dest[1]] = piece
        self.turn = 'black' if self.turn == 'white' else 'white'  
        self.moves.append(move) 
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user_id = str(uuid.uuid4())  
    users[user_id] = data['username'] 
    return jsonify({"user_id": user_id})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    for user_id, username in users.items():
        if username == data['username']:
            return jsonify({"user_id": user_id})
    return jsonify({"error": "User not found"}), 404

@app.route('/games', methods=['POST'])
def create_game():
    data = request.json
    player1, player2 = data['player1'], data['player2']
    game = Game(player1, player2)  
    games[game.id] = game 
    return jsonify({"game_id": game.id})

@app.route('/games/<game_id>', methods=['GET'])
def get_game(game_id):
    game = games.get(game_id)
    if game:
        return jsonify({
            "board": game.board,
            "turn": game.turn,
            "moves": game.moves
        })
    return jsonify({"error": "Game not found"}), 404

@app.route('/games/<game_id>/move', methods=['POST'])
def make_move(game_id):
    game = games.get(game_id)
    if game:
        move = request.json
        game.make_move(move)
        socketio.emit('update', {"game_id": game_id, "board": game.board, "turn": game.turn}, room=game_id)
        return jsonify({"status": "Move made"})
    return jsonify({"error": "Game not found"}), 404

@socketio.on('join')
def on_join(data):
    game_id = data['game_id']
    join_room(game_id) 
    emit('update', {"game_id": game_id, "board": games[game_id].board, "turn": games[game_id].turn}, room=game_id)

if __name__ == '__main__':
    socketio.run(app, debug=True) 
