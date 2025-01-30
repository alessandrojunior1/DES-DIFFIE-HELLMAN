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
    b = int(client.recv(1024).decode())
    print(f"[Sender] Chave pública do Receiver recebida: {b}")

    # Calcular chave secreta compartilhada
    shared_secret = (b**segredo) % p
    des_key = derive_des_key(shared_secret)
    
    # Converte o texto plano para bits e aplica padding
    textoPlanoBits = string_to_bits(textoPlano)
    padded_textoPlanoBits = pad_text(textoPlanoBits)

    # Cifra o texto com o DES
    encrypted_bits = []
    for i in range(0, len(padded_textoPlanoBits), 64):
        block = padded_textoPlanoBits[i:i + 64]
        encrypted_block = des_encrypt_block(block, des_key)
        encrypted_bits.extend(encrypted_block)

    # Converte os bits cifrados de volta para texto
    encrypted_text = bits_to_string(encrypted_bits)

    # Enviar texto cifrado para o Receiver
    client.send(' '.join(map(str, encrypted_bits)).encode())

    print(f"[Sender] Chave secreta compartilhada: {des_key}")
    print(f"[Sender] O texto encriptado é: {encrypted_text}")

except Exception as e:
    print(f"[Sender] Erro: {e}")
finally:
    client.close()
