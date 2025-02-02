import socket
from des import DES
from diffie_hellman import DiffieHellman

host = 'localhost'
port = 65432

g = 2
p = 23

sender = DiffieHellman(g, p)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

    client_socket.connect((host, port))
    print(f"Conectado ao servidor {host}:{port}")

    # Envia a chave pública do sender para o receiver
    client_socket.sendall(str(sender.public_key).encode())
    print(f"Chave pública do sender enviada: {sender.public_key}")

    # Recebe a chave pública do receiver
    receiver_public_key = int(client_socket.recv(1024).decode())
    print(f"Chave pública do receiver recebida: {receiver_public_key}")

    # Calcula a chave compartilhada
    shared_key = str(sender.generate_shared_key(receiver_public_key))
    # Utiliza a chave comum Diffie Hellman como a chave do DES
    des = DES(shared_key)
    # Enviar mensagem criptografada
    message = input("Enviar mensagem: ")
    encrypted_msg = des.encrypt(message)
    client_socket.sendall(encrypted_msg.encode())
    #print(f"Mensagem criptografada enviada: {encrypted_msg}")
