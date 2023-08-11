from flask import Flask, request
from flask_socketio import SocketIO, Namespace, emit
from database import add_offline_message, get_offline_messages, delete_offline_messages

app = Flask(__name__)
socketio = SocketIO(app)

class ChatNamespace(Namespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.sessions = {}  # Dictionary to store mapping of usernames to session IDs
        self.message_queue = {}  # Dictionary to store undelivered messages

    def on_connect(self):
        print("Client connected to chat namespace")

    def on_disconnect(self):
        print("Client disconnected from chat namespace")

    
    def on_register(self, data):
        print("on_register event triggered")
        self.sessions[data['username']] = request.sid
        print(f"Registered user: {data['username']}")

        # When a user comes online, check for any undelivered messages
        undelivered_messages = get_offline_messages(data['username'])
        for message in undelivered_messages:
            # Send each undelivered message to the user
            self.emit('message', message, room=request.sid)

        # Remove the undelivered messages from the database
        delete_offline_messages(data['username'])


    def on_message(self, data):
        print("Current sessions:", self.sessions)
        recipient_sid = self.sessions.get(data['recipient'])
        print("Recipient SID:", recipient_sid)
        if recipient_sid:
            self.emit('message', data['text'], room=recipient_sid)
        else:
            # If the recipient is offline, store the message in the queue
            if data['recipient'] not in self.message_queue:
                self.message_queue[data['recipient']] = []
            self.message_queue[data['recipient']].append(data['text'])

            # Store the message in the database
            # add_offline_message(data['recipient'], data['text'])


socketio.on_namespace(ChatNamespace('/chat'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
