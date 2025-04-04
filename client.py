import requests

url = "http://127.0.0.1:5000"

def check_connection():
    response = requests.get(f"{url}/connection")
    print(response.json() if response.status_code == 200 else f"Connection failed: {response.text}")

def request_word():
    response = requests.get(f"{url}/get-word")
    print(response.json() if response.status_code == 200 else f"Word request failed: {response.text}")
      
def request_int():
    response = requests.get(f"{url}/get-integer")  # Fixed endpoint name
    print(response.json() if response.status_code == 200 else f"Integer request failed: {response.text}")

def request_even(client_id):
    response = requests.post(f"{url}/get-even", json={"client_id": client_id})
    print(response.json() if response.status_code == 200 else f"Even number request failed: {response.text}")

def request_odd(client_id):
    response = requests.post(f"{url}/get-odd", json={"client_id": client_id})
    print(response.json() if response.status_code == 200 else f"Odd number request failed: {response.text}")

def pass_ident(client_id):
    response = requests.post(f"{url}/pass-ident", json={"client_id": client_id})
    print(response.json() if response.status_code == 200 else f"Identification failed: {response.text}")

def get_last_number(client_id):
    response = requests.post(f"{url}/get-last-number", json={"client_id": client_id})
    print(response.json() if response.status_code == 200 else f"Failed to get last number: {response.text}")

def main():
    check_connection()

    client_id = input("Enter client ID: ").strip()  # Ensure no accidental spaces
    pass_ident(client_id)

    get_last_number(client_id)
    #request_even(client_id)  
    request_odd(client_id)

if __name__ == "__main__":
    main()
