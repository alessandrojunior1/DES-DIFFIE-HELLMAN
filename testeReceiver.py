import socket
import random
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# Parâmetros Diffie-Hellman
p = 17
g = 3
private_key = random.randint(2, p - 2)

# Configuração do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 12345))
server.listen(1)
print("[Receiver] Aguardando conexão...")

conn, addr = server.accept()
print(f"[Receiver] Conectado a {addr}")

# Receber chave pública do Sender
A = int(conn.recv(1024).decode())

# Enviar chave pública
B = pow(g, private_key, p)
conn.send(str(B).encode())

# Calcular chave secreta compartilhada
shared_secret = pow(A, private_key, p)
des_key = shared_secret.to_bytes(8, "big")  # Chave DES de 8 bytes

# Receber e descriptografar mensagem
encrypted_message = conn.recv(1024)
cipher = DES.new(des_key, DES.MODE_ECB)
decrypted_message = unpad(cipher.decrypt(encrypted_message), 8).decode()

print(f"[Receiver] Mensagem decriptada: {decrypted_message}")

conn.close()
server.close()
