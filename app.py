## Controller for CryptoChat

from flask import Flask, render_template, request, redirect, url_for
from crypto_utils import generateKeyPair, serializePublicKey, deserializePublicKey, getSharedSecret # Utilizes crypto_utils.py

app = Flask(__name__) 

messages = [] ## stores messsages from chat.html message here temporarily

@app.route('/') ## route decorator for home page
def home():
  return render_template('index.html')

@app.route('/chat')
def chat():
  return render_template('chat.html', messages = messages) ## passess all messages into the message display

@app.route('/send', methods=['POST']) ## activated when a message is sent through POST to /send
def send_message():
  message = request.form.get('message') ## retrieves messages from form in chat.html
  if message:
    messages.append(message) # stores message in temporary array
  return redirect(url_for('chat'))

if __name__ == '__main__': ## used if file is run directly

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

  app.run(debug=True) ## starts server/if website alters, reloads 
