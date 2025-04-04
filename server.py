from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
import random


app = Flask(__name__)
client_data = {}

# Pydantic models for request validation
class ClientIDModel(BaseModel):
    client_id: str  # Ensuring client_id is always a string

@app.route('/connection', methods=['GET'])
def conection():
    """Listen for client requests."""
    return jsonify({"message": "Connected to the server"}), 200
    
@app.route('/get-word', methods=['GET'])
def get_word():
    return jsonify({"message": "Hello World"}), 200

@app.route('/get-integer', methods=['GET'])
def get_int():
    """Return an integer as a string."""
    data = convert(123456789)
    return jsonify({"integer": data}), 200

@app.route('/get-even', methods=['POST'])
def get_even():
    """Generate an even number and store it for the client."""
    try:
        data = ClientIDModel(**request.get_json())  # Validate JSON
        client_id = data.client_id
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    num_even = random.randint(1, 50) * 2
    client_data[client_id] = num_even  
    return jsonify({"even_number": num_even}), 200

@app.route('/get-odd', methods=['POST'])
def get_odd():
    """Generate an odd number and store it for the client."""
    try:
        data = ClientIDModel(**request.get_json())  
        client_id = data.client_id
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    num_odd = random.randint(1, 50) * 2 + 1
    client_data[client_id] = num_odd  
    return jsonify({"odd_number": num_odd}), 200

def convert(data):
    new_data = str(data)
    return new_data


@app.route('/pass-ident', methods=['POST'])
def save_ident():
    """Register a client ID only if it does not exist."""
    try:
        data = ClientIDModel(**request.get_json())  
        client_id = data.client_id
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    if client_id not in client_data:
        client_data[client_id] = None  
        return jsonify({"message": f"Client {client_id} registered successfully"}), 200
    else:
        return jsonify({"message": f"Client {client_id} already exists"}), 200


@app.route('/get-last-number', methods=['POST'])
def get_last_number():
    """Retrieve the last assigned number for a given client."""
    try:
        data = ClientIDModel(**request.get_json())  
        client_id = data.client_id
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    if client_id not in client_data:
        return jsonify({"error": "Client ID not found"}), 404
    
    last_number = client_data[client_id]
    if last_number is not None:
        return jsonify({"last_number": last_number}), 200
    else:
        return jsonify({"error": "Client does not have a saved number"}), 404


if __name__ == "__main__":
    app.run()