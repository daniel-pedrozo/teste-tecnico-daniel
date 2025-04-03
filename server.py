from flask import Flask, request, jsonify
import random


app = Flask(__name__)

client_data = {}

@app.route('/connection', methods=['GET'])
def conection():
    """Escutar a requisição do cliente"""
    return "Conectado ao servidor"
    
@app.route('/get-word', methods=['GET'])
def hello_word():
    data = "Hello Word"
    return data

@app.route('/get-inteiro', methods=['GET'])
def inteiro() -> int:    
    data = convert(123456789)
    return data

@app.route('/get-even', methods=['GET'])
def even():
    num_even = random.randint(1,50) * 2
    new_num = convert(num_even)
    return new_num

@app.route('/get-odd', methods=['GET'])
def odd():
    num_odd = random.randint(1,50) * 2 + 1
    new_num = convert(num_odd)
    return new_num


def convert(data):
    new_data = str(data)
    return new_data

@app.route('/pass-ident', methods=['POST'])
def save_ident():
    """Save the client's identification and assign a random number."""
    data = request.get_json()
    
    if not data or 'client_id' not in data:
        return jsonify({"error": "Client ID is required"}), 400
    
    client_id = data['client_id']
    random_number = random.randint(1, 100)

    # Store the number for the client
    client_data[client_id] = random_number

    return jsonify({"message": f"Number {random_number} assigned to client {client_id}"}), 200

@app.route('/get-last-number', methods=['POST'])
def get_last_number():
    """Retrieve the last assigned number for a given client."""
    data = request.get_json()
    
    if not data or 'client_id' not in data:
        return jsonify({"error": "Client ID is required"}), 400
    
    client_id = data['client_id']
    
    if client_id in client_data:
        return jsonify({"last_number": client_data[client_id]}), 200
    else:
        return jsonify({"error": "Client ID not found"}), 404

if __name__ == "__main__":
    app.run()