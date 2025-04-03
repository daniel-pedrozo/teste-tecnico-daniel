import requests


url = "http://127.0.0.1:5000"


def check_connection():
    response = requests.get(f"{url}/connection")
    print(response.text if response.status_code == 200 else "Connection failed")

def request_word():
    response = requests.get(f"{url}/get-word")
    print(response.text if response.status_code == 200 else "Word request failed")
      
def request_int():
    response = requests.get(f"{url}/get-inteiro")
    print(response.text if response.status_code == 200 else "Integer request failed")

def request_even():
    response = requests.get(f"{url}/get-even")
    print(response.text if response.status_code == 200 else "Even number request failed")

def request_odd():
    response = requests.get(f"{url}/get-odd")
    print(response.text if response.status_code == 200 else "Odd number request failed")
    
def pass_ident(client_id):
    response = requests.post(f"{url}/pass-ident", json={"client_id": client_id})
    print(response.json() if response.status_code == 200 else "Identification failed")

def get_last_number(client_id):
    response = requests.post(f"{url}/get-last-number", json={"client_id": client_id})
    print(response.json() if response.status_code == 200 else "Failed to get last number")

def main():
    check_connection()
    request_word()
    check_connection()
    request_int()

    client_id = input("What is the client id?")
    pass_ident(client_id)
    get_last_number(client_id)


if __name__ == "__main__":
    main()