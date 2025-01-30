import socket
import random
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# Parâmetros Diffie-Hellman
p = 17
g = 3
private_key = random.randint(2, p - 2)

# Conectar ao Receiver
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 12345))
print("[Sender] Conectado ao Receiver")

# Enviar chave pública
A = pow(g, private_key, p)
client.send(str(A).encode())

# Receber chave pública de Bob
B = int(client.recv(1024).decode())

# Calcular chave secreta compartilhada
shared_secret = pow(B, private_key, p)
des_key = shared_secret.to_bytes(8, "big")  # Chave DES de 8 bytes

# Criptografar mensagem
textoPlano = input("Digite um texto: ")
cipher = DES.new(des_key, DES.MODE_ECB)
encrypted_message = cipher.encrypt(pad(textoPlano.encode(), 8))

# Enviar mensagem criptografada
client.send(encrypted_message)

print(f"[Sender] Mensagem criptografada enviada!{encrypted_message.hex()}")
client.close()
