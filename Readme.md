Aplicação Cliente-Servidor
Contexto

    Estrutura cliente-servidor
    Expansível
    Único canal de comunicação

Requisitos

    Flask
    Requisito HTTP
    Interface / comunicação

**Estrutura**

 Servidor (Servidor.py)
 
     Mandar (msg)
     Receber (msg)
     Comunicação HTTP
     Método gera números aleatórios pares
     Métodos gera números aleatórios ímpares
     Método para verificar identificação do cliente
 
 Cliente (Cliente.py)
 
     Escutar servidor
     Input usuário
     Leitura de msg
     Ao vivo

**Requisitos**

Cliente

    Cliente vai requisitar -> "hello word" e int para o servidor
    Servidor irá responder com as informações adequadas


**Docker**

To run 
    docker compose up --build

To stop
    docker compose down

To see the logs
    docker compose logs -f server
    docker compose logs -f even
    docker compose logs -f odd


**Errors to fix**
    The valid.sh is not runing when used docker compose up -build
    The test_server is not working