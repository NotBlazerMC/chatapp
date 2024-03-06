from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat/<username>')
def chat(username):
    return render_template('chat.html', username=username)

@socketio.on('join')
def handle_join(data):
    username = data['username']
    join_room(username)
    emit('message', {'sender': 'SERVER', 'message': f'{username} joined the chat'}, room=username)

@socketio.on('message')
def handle_message(data):
    sender = data['sender']
    message = data['message']
    emit('message', {'sender': sender, 'message': message}, room=sender)

if __name__ == '__main__':
    socketio.run(app, debug=True)
