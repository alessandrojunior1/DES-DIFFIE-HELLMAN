import socket
from des import DES
from diffie_hellman import DiffieHellman
import struct  # Para empacotar/desempacotar o tamanho do arquivo

# Inicializa Diffie-Hellman para troca de chaves
dh = DiffieHellman()
public_key = dh.generate_public_key()

# Conectar ao receiver e trocar chaves
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 12345))
sock.send(str(public_key).encode())

# Receber a chave pública do receiver
receiver_public_key = int(sock.recv(1024).decode())
shared_key = dh.generate_shared_key(receiver_public_key)
print(f"Chave compartilhada: {shared_key}")  # Debug

# Inicializa DES com a chave derivada
des = DES(shared_key.to_bytes(8, 'big'))

# Ler e criptografar arquivo
with open('arquivo.txt', 'rb') as f:
    file_data = f.read()
print(file_data)
print(des.encrypt(file_data))
encrypted_data = des.encrypt(file_data)

# Enviar tamanho do arquivo antes dos dados
file_size = len(encrypted_data)
sock.send(struct.pack("!I", file_size))  # Envia 4 bytes com o tamanho
print(f"Tamanho do arquivo enviado: {file_size} bytes")  # Debug

# Enviar o arquivo criptografado
sock.sendall(encrypted_data)
sock.close()
print("Arquivo enviado com sucesso!")
