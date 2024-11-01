## Controller for CryptoChat

from flask import Flask, render_template, request, redirect, url_for, jsonify
from crypto_utils import (
  generateKeyPair, serializePublicKey, deserializePublicKey, 
  getSharedSecret, encryptMessage, decryptMessage) # Utilizes crypto_utils.py

app = Flask(__name__) 

messages = [] ## stores messsages from chat.html message here temporarily

# Testing shared secret exchange
privateKey1, publicKey1 = generateKeyPair()
privateKey2, publicKey2 = generateKeyPair()

serializePublicKey1 = serializePublicKey(publicKey1)
serializePublicKey2 = serializePublicKey(publicKey2)

deserializePublicKey1 = deserializePublicKey(serializePublicKey1)
deserializePublicKey2 = deserializePublicKey(serializePublicKey2)

sharedSecret1 = getSharedSecret(privateKey1, deserializePublicKey2)
sharedSecret2 = getSharedSecret(privateKey2, deserializePublicKey1)

assert sharedSecret1 == sharedSecret2, "Shared Secrets are not the same!"
print("Shared secret established successfully!")

@app.route('/') ## route decorator for home page
def home():
  return render_template('index.html')

@app.route('/chat')
def chat():
  decryptedMessages = []
  for iv, ciphertext, tag in messages: 
    # Decrypt each message and append to decryptedMessages 
    plaintext = decryptMessage(sharedSecret1, iv, ciphertext, tag)
    decryptedMessages.append(plaintext)
  return render_template('chat.html', messages = decryptedMessages) ## passes all messages into the message display

@app.route('/send', methods=['POST']) ## activated when a message is sent through POST to /send
def send_message():
  message = request.form.get('message') ## retrieves messages from form in chat.html
  if message:

    # THIS IS WHERE WE ENCRYPT THE MESSAGE!!!#
    iv, ciphertext, tag = encryptMessage(sharedSecret1, message)
    messages.append((iv, ciphertext, tag)) # stores encrypted message, along with iv and tag, in array as a tuple

  return redirect(url_for('chat'))

@app.route('/messages') # Use JQuery to reload messages
def get_messages():
  return jsonify(messages)


if __name__ == '__main__': ## used if file is run directly

  app.run(host='0.0.0.0', port=5000, debug=True) ## starts server

 