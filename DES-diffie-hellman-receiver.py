import socket
import random
from DES import *

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
    a = int(conn.recv(1024).decode().strip())  # Remove espaços extras
    print(f"[Receiver] Chave pública de Sender recebida: {a}")

    # Enviar chave pública do Receiver
    B = (i**segredo) % p
    conn.send(str(B).encode())

    # Calcular chave secreta compartilhada
    shared_secret = (a**segredo) % p
    binary_secret = bin(shared_secret)[2:].zfill(56)[-56:]  # Garante 56 bits
    des_key = [int(bit) for bit in binary_secret]

    # Receber o tamanho da mensagem cifrada
    encrypted_size = int(conn.recv(16).decode().strip())
    conn.send(b'OK')  # Confirma recebimento do tamanho

    # Receber a mensagem cifrada completa
    data_buffer = ""
    while len(data_buffer.split()) < encrypted_size:
        chunk = conn.recv(1024).decode()
        if not chunk:
            break
        data_buffer += chunk.strip() + " "

    # Processar a string recebida e converter para lista de inteiros
    encrypted_message = list(map(int, data_buffer.strip().split()))

    # Descriptografar a mensagem completa com o DES
    decrypted_text = des_decrypt(encrypted_message, des_key).strip()

    print(f"[Receiver] Chave secreta compartilhada: {des_key}")
    print(f"[Receiver] O texto decriptado é: {decrypted_text}")

except Exception as e:
    print(f"[Receiver] Erro: {e}")
finally:
    conn.close()
    server.close()
