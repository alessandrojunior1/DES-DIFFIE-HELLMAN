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
    a = int(conn.recv(1024).decode())  # Recebe chave pública de Sender
    print(f"[Receiver] Chave pública de Sender recebida: {a}")

    # Enviar chave pública do Receiver
    B = (i**segredo) % p
    conn.send(str(B).encode())

    # Calcular chave secreta compartilhada
    shared_secret = (a**segredo) % p
    des_key = derive_des_key(shared_secret)

    # Receber a mensagem cifrada
    encrypted_message = list(map(int, conn.recv(1024).decode().split()))
    
    # Descriptografar a mensagem por blocos
    decrypted_bits = []
    for i in range(0, len(encrypted_message), 64):
        block = encrypted_message[i:i + 64]
        decrypted_block = des_decrypt_block(block, des_key)
        decrypted_bits.extend(decrypted_block)

    # Remover padding do texto decriptado
    decrypted_bits = unpad_text(decrypted_bits)
    decrypted_text = bits_to_string(decrypted_bits)

    print(f"[Receiver] Chave secreta compartilhada: {des_key}")
    print(f"[Receiver] O texto decriptado é: {decrypted_text}")

except Exception as e:
    print(f"[Receiver] Erro: {e}")
finally:
    conn.close()
    server.close()
