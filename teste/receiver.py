import socket
from des import DES
from diffie_hellman import DiffieHellman
import struct  # Para empacotar/desempacotar o tamanho do arquivo

# Inicializa Diffie-Hellman para troca de chaves
dh = DiffieHellman()
public_key = dh.generate_public_key()

# Criar socket e aguardar conexão
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 12345))
sock.listen(1)
conn, addr = sock.accept()

# Receber chave pública do sender e enviar a própria chave pública
sender_public_key = int(conn.recv(1024).decode())
conn.send(str(public_key).encode())

# Gerar chave compartilhada
shared_key = dh.generate_shared_key(sender_public_key)
print(f"Chave compartilhada: {shared_key}")  # Debug

# Inicializa DES com a chave derivada
des = DES(shared_key.to_bytes(8, 'big'))

# 🟢 Receber primeiro os 4 bytes que indicam o tamanho do arquivo criptografado
file_size_data = conn.recv(4)
file_size = struct.unpack("!I", file_size_data)[0]  # Converte para int
print(f"Tamanho esperado do arquivo: {file_size} bytes")  # Debug

# 🟢 Agora recebemos os dados até completar o tamanho esperado
received_data = b""
while len(received_data) < file_size:
    chunk = conn.recv(min(1024, file_size - len(received_data)))  # Evita excessos
    if not chunk:
        break
    received_data += chunk

conn.close()

print(f"Tamanho real recebido: {len(received_data)} bytes")  # Debug
print(received_data)
# 🟢 Descriptografar e salvar
decrypted_data = des.decrypt(received_data)
print(f"Tamanho descriptografado: {len(decrypted_data)} bytes")  # Debug

with open('arquivo_recebido.txt', 'wb') as f:
    f.write(decrypted_data)
print(decrypted_data)

print("Arquivo recebido e descriptografado com sucesso! 🎉")
