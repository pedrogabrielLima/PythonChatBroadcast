import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# Inicializa a cor
init()

# Grupo das cores disponíveis
colors = [
    Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, Fore.LIGHTBLUE_EX,
    Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX, Fore.MAGENTA,
    Fore.RED, Fore.WHITE, Fore.YELLOW
]

# Escolhe uma cor aleatória para o cliente
client_color = random.choice(colors)

# Endereço IP do servidor
# OBS.: Se o servidor não estiver na máquina local,
# colocar o endereço IP da rede privada (ex: 192.168.1.2)
SERVER_HOST = "192.168.0.6"
# Porta de conexão com o servidor
SERVER_PORT = 5002

# Utilizado para separar o nome do cliente da mensagem
separator_token = "<SEP>"

# Inicializa o socket TCP
s = socket.socket()
print(f"[*] Conectando ao {SERVER_HOST}:{SERVER_PORT}...")
# Conecta ao servidor
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Conectado.")
# Entrada do nome do cliente
name = input("Digite seu nome: ")

# Método listen para as mensagens
def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

# Cria uma thread para o método listen
t = Thread(target=listen_for_messages)
# Cria uma trhead deamon para que quando a thead main terminar, ela também termine
t.daemon = True
# Inicializa a thread
t.start()

while True:
    # Entrada da mensagem a ser enviada para o servidor
    to_send = input()
    # Condição para sair do programa
    if to_send.lower() == 'q':
        break
    # Adiciona o datetime, nome, e a cor de quem envia a mensagem
    date_now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # Envia a mensagem
    s.send(to_send.encode())

# Fecha o socket
print("Saindo do chat\n")
s.close()
