from flask import Flask, render_template

app = Flask(__name__) 

@app.route('/') ## route decorator for home page
def home():
  return render_template('index.html')

@app.route('/chat')
def chat():
  return render_template('chat.html')

if __name__ == '__main__': ## used if file is run directly
  app.run(debug=True) ## starts server/if website alters, reloads 
