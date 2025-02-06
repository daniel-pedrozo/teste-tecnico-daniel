from flask import Flask, request
import random


app = Flask(__name__)

#registra o ID e o token
data_base: dict = {}

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

@app.route('/get-par', methods=['GET'])
def par():
    num_par = random.randint(1,50) * 2
    new_num = convert(num_par)
    return new_num

@app.route('/get-impar', methods=['GET'])
def impar():
    num_impar = random.randint(1,50) * 2 + 1
    new_num = convert(num_impar)
    return new_num

@app.route('pass-ident', methods=['POST'])
def save_ident():
    ...

def convert(data):
    new_data = str(data)
    return new_data


if __name__ == "__main__":
    app.run()