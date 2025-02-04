from util import clear_terminal
import socket
from des import DES
from diffie_hellman import DiffieHellman

# Configuração do servidor
host = 'localhost'
port = 65432

# Parâmetros públicos (g e p)
g = 2
p = 23

# Inicializando o receiver (servidor) Diffie-Hellman
receiver = DiffieHellman(g, p)

# Cria uma comunicação via socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    clear_terminal()
    server_socket.bind((host, port)) 
    server_socket.listen(1)
    print(f"\nAguardando conexão na porta {port}...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Conectado a: {addr}")
        
        while True:
            # Recebe a chave pública de Sender
            data = conn.recv(1024).decode()
            if not data:
                print("\nConexão encerrada pelo sender.")
                break
            sender_public_key = int(data)
            print(f"\nChave pública do sender recebida: {sender_public_key}")

            # Envia a chave pública de Receiver para Sender
            conn.sendall(str(receiver.public_key).encode())
            print(f"Chave pública do receiver enviada: {receiver.public_key}")

            # Calcula a chave compartilhada
            shared_key = str(receiver.generate_shared_key(sender_public_key))
        
            # Utiliza a chave comum Diffie Hellman como a chave do DES
            des = DES(shared_key)
            # Recebe a mensagem criptografada
            encrypted_msg = conn.recv(1024).decode()
            print(f"\nMensagem criptografada recebida: {encrypted_msg}")
            print(f"\nMensagem descriptografada: {des.decrypt(encrypted_msg)}\n")
print("\nChat encerrado.\n")