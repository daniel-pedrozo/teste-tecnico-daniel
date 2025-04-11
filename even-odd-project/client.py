import argparse

import requests

BASE_URL = "http://127.0.0.1:8000"


def handle_request(method, endpoint, client_id=None, json=None, label=None):
    url = f"{BASE_URL}/{endpoint}"
    params = {"client_id": client_id} if client_id else None

    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=json)
        else:
            raise ValueError(f"Unsupported method: {method}")
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return

    if response.status_code == 200:
        print(f"{label}:", response.json())
    else:
        print(f"{label} failed: {response.status_code} - {response.text}")


def check_connection():
    handle_request("GET", "conection", label="Connection check")


def request_even(client_id):
    handle_request("GET", "get_even", client_id=client_id, label="Even number response")


def request_odd(client_id):
    handle_request("GET", "get_odd", client_id=client_id, label="Odd number response")


def pass_ident(client_id):
    handle_request(
        "POST",
        "register-client",
        json={"client_id": client_id},
        label="Client ID registration",
    )


def get_last_number(client_id):
    handle_request("GET", "last-number", client_id=client_id, label="Last number")


def get_history(client_id):
    handle_request("GET", "get-history", client_id=client_id, label="Number history")


def main():
    parser = argparse.ArgumentParser(
        description="Client to interact with the server and services."
    )
    parser.add_argument("client_id", help="Client ID to use in all requests")

    parser.add_argument(
        "-r", "--register", action="store_true", help="Register the client ID"
    )
    parser.add_argument(
        "-e", "--even", action="store_true", help="Request an even number"
    )
    parser.add_argument(
        "-o", "--odd", action="store_true", help="Request an odd number"
    )
    parser.add_argument(
        "-l", "--last", action="store_true", help="Get the last stored number"
    )
    parser.add_argument(
        "-p", "--past", action="store_true", help="Get the number history"
    )

    args = parser.parse_args()

    check_connection()

    client_id = args.client_id

    if args.register:
        pass_ident(client_id)
    if args.even:
        request_even(client_id)
    if args.odd:
        request_odd(client_id)
    if args.last:
        get_last_number(client_id)
    if args.past:
        get_history(client_id)


if __name__ == "__main__":
    main()
