from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Enable debug mode
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def home():   
    return render_template('./home/home.html')

@app.route('/sign_up')
def sign_up():
    return render_template('home/sign_up.html')

@app.route('/sign_in')
def sign_in():
    return render_template('home/sign_in.html')


@app.route('/dashboard')
def dashboard():
    with open('response.json', 'r') as f:
        decks = json.load(f)
    return render_template('dashboard.html', decks=decks)

@app.route('/flashcards/<topic>')
def flashcards(topic):
    with open('response.json', 'r') as f:
        deck = json.load(f)
    if deck['topic'] == topic:
        return render_template('flashcards.html', deck=deck)
    else:
        return "Deck not found", 404

@app.route('/api/deck/<topic>')
def get_deck(topic):
    with open('response.json', 'r') as f:
        deck = json.load(f)
    if deck['topic'] == topic:
        return jsonify(deck)
    else:
        return "Deck not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=True)