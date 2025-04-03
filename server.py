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
def int() -> int:    
    data = convert(123456789)
    return data

@app.route('/get-even', methods=['POST'])
def even():
    """Generate an even number and store it for the client."""
    data = request.get_json()
    
    if not data or 'client_id' not in data:
        return jsonify({"error": "Client ID is required"}), 400
    
    client_id = data['client_id']
    num_even = random.randint(1, 50) * 2
    client_data[client_id] = num_even  # Save the number for this client
    
    return jsonify({"even_number": num_even})

@app.route('/get-odd', methods=['POST'])
def odd():
    """Generate an odd number and store it for the client."""
    data = request.get_json()
    
    if not data or 'client_id' not in data:
        return jsonify({"error": "Client ID is required"}), 400
    
    client_id = data['client_id']
    num_odd = random.randint(1, 50) * 2 + 1
    client_data[client_id] = num_odd  # Save the number for this client
    
    return jsonify({"odd_number": num_odd})


def convert(data):
    new_data = str(data)
    return new_data


@app.route('/pass-ident', methods=['POST'])
def save_ident():
    """Register a client ID only if it does not exist."""
    data = request.get_json()
    
    if not data or 'client_id' not in data:
        return jsonify({"error": "Client ID is required"}), 400
    
    client_id = data['client_id']

    # Only register if the client does not exist
    if client_id not in client_data:
        client_data[client_id] = None  # Placeholder for future numbers
        return jsonify({"message": f"Client {client_id} registered successfully"}), 200
    else:
        return jsonify({"message": f"Client {client_id} already exists, keeping previous data"}), 200


@app.route('/get-last-number', methods=['POST'])
def get_last_number():
    """Retrieve the last assigned number for a given client."""
    data = request.get_json()
    
    if not data or 'client_id' not in data:
        return jsonify({"error": "Client ID is required"}), 400
    
    client_id = data['client_id']

    if client_data[client_id]:
    
        if client_id in client_data:
            return jsonify({"last_number": client_data[client_id]}), 200
        else:
            return jsonify({"error": "Client ID not found"}), 404
    else:
        return jsonify({"error": "Client does not have a saved number"})

if __name__ == "__main__":
    app.run()