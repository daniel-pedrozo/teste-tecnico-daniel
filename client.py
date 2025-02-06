import requests


url = "http://127.0.0.1:5000"


def check_connection() ->None:
    response = requests.get("http://127.0.0.1:5000/connection")
    if response.status_code == 200:
        print(response.text)
        
    else:
        print("Informações nao encontradas")
    
def request_word() ->None:
    response = requests.get("http://127.0.0.1:5000/get-word")
    if response.status_code == 200:

        print(response.text)
    else:
        print("Informações nao encontradas")
        
def request_int() ->None:
    response = requests.get("http://127.0.0.1:5000/get-inteiro")
    if response.status_code == 200:
        print(response.text)
    else:
        print("Informações nao encontradas")
    
def pass_ident(data) ->None:
    response = requests.post("http://127.0.0.1:5000/pass-ident", data=data)
    
    
def main() ->None:
    check_connection()
    request_word()
    check_connection()
    request_int()
    pass_ident(data=101)


if __name__ == "__main__":
    main()