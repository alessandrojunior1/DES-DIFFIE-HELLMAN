import socket
import random


p = 17
i = 3

segredo = random.randint(2, p-2)

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 12345))
server.listen(1)
print("[Receiver] Aguardando conexão...")

try:
    conn, addr = server.accept()
    print(f"[Receiver] Conectado a {addr}")

    # Receber chave pública do Sender
    a = int(conn.recv(1024).decode())  # Recebe chave pública de Sender
    print(f"[Receiver] Chave pública de Sender recebida: {a}")

    # Enviar chave pública do Receiver
    b = (i**segredo) % p
    conn.send(str(b).encode())

    # Calcular chave secreta compartilhada
    shared_secret = (a**segredo) % p
    print(f"[Receiver] Chave secreta compartilhada: {shared_secret}")

except Exception as e:
    print(f"[Receiver] Erro: {e}")
finally:
    conn.close()
    server.close()
