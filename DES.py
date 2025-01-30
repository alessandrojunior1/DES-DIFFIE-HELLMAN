
# Tabelas utilizadas pelo DES
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17,  9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41,  9, 49, 17, 57, 25]

def permute(block, table):
    """Realiza a permutação de acordo com a tabela fornecida."""
    return [block[i - 1] for i in table]

def xor(a, b):
    """XOR bit a bit entre duas listas."""
    return [i ^ j for i, j in zip(a, b)]

def string_to_bits(s):
    """Converte uma string em uma lista de bits."""
    return [int(b) for c in s for b in format(ord(c), '08b')]

def bits_to_string(b):
    """Converte uma lista de bits de volta para uma string."""
    return ''.join(chr(int(''.join(map(str, b[i:i+8])), 2)) for i in range(0, len(b), 8))

def pad_text(text_bits):
    """Adiciona padding para que o texto tenha um tamanho múltiplo de 64 bits."""
    while len(text_bits) % 64 != 0:
        text_bits.append(0)  # Adiciona 0 até o tamanho ser múltiplo de 64
    return text_bits

def unpad_text(text_bits):
    """Remove o padding do texto depois da decifra."""
    while text_bits and text_bits[-1] == 0:
        text_bits.pop()  # Remove os 0s de padding
    return text_bits

def des_encrypt_block(block, key):
    """Cifra um bloco de 64 bits com a chave de 56 bits."""
    block = permute(block, IP)
    L, R = block[:32], block[32:]
    
    for i in range(16):
        round_key = key[i % len(key):] + key[:i % len(key)]  # Gera uma subchave simples
        new_R = xor(L, xor(R, round_key[:32]))
        L, R = R, new_R
    
    combined = L + R
    return permute(combined, IP_INV)

def des_decrypt_block(block, key):
    """Descriptografa um bloco de 64 bits com a chave de 56 bits."""
    block = permute(block, IP)
    L, R = block[:32], block[32:]
    
    for i in reversed(range(16)):
        round_key = key[i % len(key):] + key[:i % len(key)]  # Gera a subchave na ordem inversa
        new_L = xor(R, xor(L, round_key[:32]))
        R, L = L, new_L
    
    combined = L + R
    return permute(combined, IP_INV)


def derive_des_key(shared_secret):
    """Deriva uma chave de 56 bits a partir da chave compartilhada Diffie-Hellman."""
    binary_secret = bin(shared_secret)[2:][-56:]  # Pega os 56 bits menos significativos
    return [int(bit) for bit in binary_secret.zfill(56)]


