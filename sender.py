from util import clear_terminal
import socket
from des import DES
from diffie_hellman import DiffieHellman

host = 'localhost'
port = 65432

g = 2
p = 23

sender = DiffieHellman(g, p)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    clear_terminal()
    client_socket.connect((host, port))
    print(f"\nConectado ao servidor {host}:{port}")

    while True:
        # Envia a chave pública do sender para o receiver
        client_socket.sendall(str(sender.public_key).encode())
        print(f"\nChave pública do sender enviada: {sender.public_key}")

        # Recebe a chave pública do receiver
        receiver_public_key = int(client_socket.recv(1024).decode())
        print(f"Chave pública do receiver recebida: {receiver_public_key}\n")

        # Calcula a chave compartilhada
        shared_key = str(sender.generate_shared_key(receiver_public_key))

        # Utiliza a chave comum Diffie Hellman como a chave do DES
        des = DES(shared_key)

        # Enviar mensagem criptografada
        message = input("Enviar mensagem: ")
        encrypted_msg = des.encrypt(message)
        client_socket.sendall(encrypted_msg.encode())
        print(f"\nMensagem criptografada enviada: {encrypted_msg}\n")

        c = input("\nDeseja encerrar o chat? (S/n):")
        if c.lower() == 's':
            client_socket.close()
            break
print("\nChat encerrado.\n")
        
