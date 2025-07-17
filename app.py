from flask import Flask, request, jsonify, send_file
import json
import os

app = Flask(__name__)
DATA_FILE = 'players.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/submit-score', methods=['POST'])
def submit_score():
    data = request.json
    name = data.get('name')
    wallet = data.get('wallet')
    score = int(data.get('score', 0))

    if score >= 15:
        with open(DATA_FILE, 'r') as f:
            players = json.load(f)

        players = [p for p in players if p['wallet'] != wallet]
        players.append({'name': name, 'wallet': wallet, 'score': score})

        with open(DATA_FILE, 'w') as f:
            json.dump(players, f, indent=2)

        return jsonify({'status': 'saved'})
    else:
        return jsonify({'status': 'ignored'})

@app.route('/download', methods=['GET'])
def download():
    return send_file(DATA_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run()
