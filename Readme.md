
-- Contexto:
- estrutura cliente servidor;
- expandivel;
- unico canal de comunicação ;

--- Aplição Cliente Servidor ---

 -- Requisitos:
    Flask;
    Requisito HTTP;
    Interface / comunicação;

-- Estrutura:
    Servidor.py
        - Mandar (msg);
        - Receber (msg);
        - Comunicação HTTP;
        - Metodo Gera numeros aleatorios pares;
        - Metodos gera numeros aleatorios impares;
        - Metodo para verificar indentificação do cliente


    Cliente.py
        - Escutar servidor;
        - Input usuario;
        - Leitura de msg;
        - Ao vivo;

-- requisitos:
    - cliente:
        - Cliente vai requisitar -> "hello word" e int para o servidor;
        - Servidor ira responder com as informações adquadas;