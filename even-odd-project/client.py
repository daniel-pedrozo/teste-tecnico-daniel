import requests

BASE_URL = "http://127.0.0.1:5000"


def check_connection():
    response = requests.get(f"{BASE_URL}/connection")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Connection failed: {response.status_code} - {response.text}")


def request_even(client_id):
    response = requests.post(f"{BASE_URL}/get-even", json={"client_id": client_id})
    if response.status_code == 200:
        print("Even number response:", response.json())
    else:
        print(
            f"Even number request failed in: {response.status_code} - {response.text}"
        )


def request_odd(client_id):
    response = requests.post(f"{BASE_URL}/get-odd", json={"client_id": client_id})
    if response.status_code == 200:
        print("Odd number response:", response.json())
    else:
        print(f"Odd number request failed: {response.status_code} - {response.text}")


def pass_ident(client_id):
    response = requests.post(f"{BASE_URL}/pass-ident", json={"client_id": client_id})
    if response.status_code == 200:
        print("Client ID registration:", response.json())
    else:
        print(f"Identification failed: {response.status_code} - {response.text}")


def get_last_number(client_id):
    response = requests.post(
        f"{BASE_URL}/get-last-number", json={"client_id": client_id}
    )
    if response.status_code == 200:
        print("Last number:", response.json())
    else:
        print(f"Failed to get last number: {response.status_code} - {response.text}")


def get_history(client_id):
    response = requests.post(f"{BASE_URL}/get-history", json={"client_id": client_id})
    if response.status_code == 200:
        print("Number history:", response.json())
    else:
        print(f"Failed to get history: {response.status_code} - {response.text}")


def main():
    check_connection()
    # just to make the processes of sending a new client id easier
    client_id = input("What is the client id:")

    pass_ident(client_id)

    get_history(client_id)
    """get_last_number(client_id)

    request_even(client_id)
    request_odd(client_id)
    get_last_number(client_id)"""


if __name__ == "__main__":
    main()
