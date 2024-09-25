from flask import Flask, render_template, jsonify
from langchain.prompts import PromptTemplate
import json


app = Flask(__name__)

@app.route('/')
def home():   
    return render_template('index.html')

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
    app.run(host="0.0.0.0", port=5000, debug=True)