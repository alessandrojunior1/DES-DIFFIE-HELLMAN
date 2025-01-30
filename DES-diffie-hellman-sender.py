import socket
import random
from DES import *

p = 17
i = 3

segredo = random.randint(2, p-2)

# Conectar ao Receiver   
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(("localhost", 12345))
    print("[Sender] Conectado ao Receiver")
    textoPlano = input("Digite um texto: ")

    # Enviar chave pública para o Receiver
    A = (i**segredo) % p
    client.send(str(A).encode())

    # Receber chave pública do Receiver
    b = int(client.recv(1024).decode().strip())
    print(f"[Sender] Chave pública do Receiver recebida: {b}")

    # Calcular chave secreta compartilhada
    shared_secret = (b**segredo) % p
    binary_secret = bin(shared_secret)[2:][-56:].zfill(56)  # Garante 56 bits
    des_key = [int(bit) for bit in binary_secret]

    # Cifra o texto com o DES
    encrypted_bits = des_encrypt(textoPlano, des_key)
    
    # Enviar o tamanho da mensagem cifrada
    client.send(str(len(encrypted_bits)).encode())
    
    # Aguarda confirmação do receiver
    if client.recv(16).decode().strip() != 'OK':
        raise Exception("Erro ao sincronizar com o Receiver.")

    # Enviar os bits cifrados
    client.send(' '.join(map(str, encrypted_bits)).encode())

    print(f"[Sender] Chave secreta compartilhada: {des_key}")
    print(f"[Sender] O texto encriptado foi enviado com sucesso.")

except Exception as e:
    print(f"[Sender] Erro: {e}")
finally:
    client.close()
