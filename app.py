## Controller for CryptoChat

from flask import Flask, render_template, request, redirect, url_for

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
  app.run(debug=True) ## starts server/if website alters, reloads 
