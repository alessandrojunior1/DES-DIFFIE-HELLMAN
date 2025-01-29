import socket
import random

p = 17
i = 3

segredo = random.randint(2, p-2)

# Conectar ao Receiver
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(("localhost", 12345))
    print("[Sender] Conectado ao Receiver")

    # Enviar chave pública para o Receiver
    A = (i**segredo) % p
    client.send(str(A).encode())

    # Receber chave pública do Receiver
    b = int(client.recv(1024).decode())
    print(f"[Sender] Chave pública do Receiver recebida: {b}")

    # Calcular chave secreta compartilhada
    shared_secret = (b**segredo) % p
    print(f"[Sender] Chave secreta compartilhada: {shared_secret}")

except Exception as e:
    print(f"[Sender] Erro: {e}")
finally:
    client.close()
