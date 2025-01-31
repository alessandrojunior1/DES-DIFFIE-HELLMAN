import socket
import random
from DES import *

p = 17
i = 3

segredo = random.randint(2, p-2)

# Configuração do cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 12345))
print("[Sender] Conectado ao Receiver")

# Enviar chave pública do Sender
a = (i**segredo) % p
client.send(str(a).encode())

# Receber chave pública do Receiver
B = int(client.recv(1024).decode().strip())  # Remove espaços extras
print(f"[Sender] Chave pública do Receiver recebida: {B}")

# Calcular chave secreta compartilhada
shared_secret = (B**segredo) % p
binary_secret = bin(shared_secret)[2:].zfill(64)[-64:]  # Garante 64 bits
des_key = [int(bit) for bit in binary_secret]

# Solicitar ao usuário uma mensagem e criptografá-la
message = input("Digite um texto: ").strip()

# Cifrar a mensagem com o DES
encrypted_message = des_encrypt(message, des_key)

# Enviar o tamanho da mensagem cifrada
client.send(str(len(encrypted_message)).encode())

# Aguardar confirmação
temp_response = client.recv(1024)

# Enviar a mensagem cifrada
for chunk in range(0, len(encrypted_message), 1024):
    client.send(" ".join(map(str, encrypted_message[chunk:chunk+1024])).encode())

print("[Sender] Mensagem cifrada enviada com sucesso.")

client.close()
