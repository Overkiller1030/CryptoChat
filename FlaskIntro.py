from flask import Flask, render_template, request ## intializes Flask, uses template folder for HTML, 
"""
from flask_socketio import SocketIO, emit
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
"""

app = Flask(__name__) ## Initializes Flask

@app.route("/")
def home():
  return render_template('index.html')

@app.route('/submit', methods=['POST']) ## Once data is sent to backend, routed to another page
def submit():
  username = request.form['username']
  return f'Hello, {username}!' ## Where you are greeted

if __name__ == '__main__':
  app.run(debug=True) ## Runs app in debug mode
