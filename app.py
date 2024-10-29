from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from crypto_utils import (
    generateKeyPair, serializePublicKey, deserializePublicKey, 
    getSharedSecret, encryptMessage, decryptMessage)

app = Flask(__name__)
socketIO = SocketIO(app)

messages = []

# Keys setup
privateKey1, publicKey1 = generateKeyPair()
privateKey2, publicKey2 = generateKeyPair()
sharedSecret1 = getSharedSecret(privateKey1, deserializePublicKey(serializePublicKey(publicKey2)))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    decrypted_messages = [{'plaintext': decryptMessage(sharedSecret1, iv, ciphertext, tag), 
                           'ciphertext': (iv.hex(), ciphertext.hex(), tag.hex())} for iv, ciphertext, tag in messages]
    return render_template('chat.html', messages=decrypted_messages)

@app.route('/send', methods=['POST'])
def send_message():
    message = request.form.get('message')
    if message:
        iv, ciphertext, tag = encryptMessage(sharedSecret1, message)
        messages.append((iv, ciphertext, tag))
        socketIO.emit('receive_message', {
            'plaintext': message,
            'ciphertext': (iv.hex(), ciphertext.hex(), tag.hex())
        })
    return redirect(url_for('chat'))

if __name__ == '__main__':
    socketIO.run(app, host='0.0.0.0', port=5000, debug=True)
