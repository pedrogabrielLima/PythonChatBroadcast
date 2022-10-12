import socket
from threading import Thread

# Endereço IP do servidor
SERVER_HOST = "192.168.0.6"
# Porta de conexão do servidor
SERVER_PORT = 5002
# Utilizado para separar o nome do cliente da mensagem
separator_token = "<SEP>"

# Inicializa a lista de sockets de todos os clientes conectados
client_sockets = set()
# Cria um socket TCP
s = socket.socket()
# Faz com que a porta seja reutilizada
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Faz o bind na porta e IP passados acima
s.bind((SERVER_HOST, SERVER_PORT))
# Inicia o listen para as conexões futuras
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):

    """
    Essa função faz o listen das mensagens vindas do socket 'cs'
    Independente de quando a mensagem é recebida, ela é enviada a todos
    os clientes conectados.
    """

    while True:
        try:
            # Continua fazendo o listening das mensagens vindas do socket 'cs'
            msg = cs.recv(1024).decode()
            print(msg.replace(separator_token, ": "))
        except Exception as e:
            # Cliente não está mais conectado
            # remover cliente da lista
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # Trocando o separador <SEP> para ": ", melhorando a visualização
            msg = msg.replace(separator_token, ": ")
        # Percorre toda a lista de sockets dos clientes conectados
        for client_socket in client_sockets:
            # Envia a mensagem
            client_socket.send(msg.encode())


while True:
    # Continua fazendo o listening das mensagens
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # Adiciona o novo cliente conectado a lista de clientes
    client_sockets.add(client_socket)
    # Inicia uma nova thread que executa o listen para a mensagem de cada cliente
    t = Thread(target=listen_for_client, args=(client_socket,))
    # Cria uma trhead deamon para que quando a thead main terminar, ela também termine
    t.daemon = True
    # Inicializa a thread
    t.start()

# Fecha todos os sockets dos clientes
for cs in client_sockets:
    cs.close()
# Fecha o socket do servidor
s.close()
