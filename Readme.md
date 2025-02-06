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
