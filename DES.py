
# Tabelas utilizadas pelo DES
ip_table = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]
    # PC1 permutation table
pc1_table = [
        57, 49, 41, 33, 25, 17, 9, 1,
        58, 50, 42, 34, 26, 18, 10, 2,
        59, 51, 43, 35, 27, 19, 11, 3,
        60, 52, 44, 36, 63, 55, 47, 39,
        31, 23, 15, 7, 62, 54, 46, 38,
        30, 22, 14, 6, 61, 53, 45, 37,
        29, 21, 13, 5, 28, 20, 12, 4
    ]
    # Define the left shift schedule for each round
shift_schedule = [1, 1, 2, 2,
                      2, 2, 2, 2,
                      1, 2, 2, 2,
                      2, 2, 2, 1]

    # PC2 permutation table
pc2_table = [
        14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32
    ]
    #expension
e = [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]

    # S-box tables for DES
S_boxes = [
        # S-box 1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        # S-box 2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        # S-box 3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        # S-box 4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        # S-box 5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        # S-box 6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        # S-box 7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        # S-box 8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]
p = [
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    ]
ip_inverse = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25
    ]
def permute(bits, table):
    return [bits[i - 1] for i in table]

def xor(a, b):
    return [i ^ j for i, j in zip(a, b)]

def string_to_bits(message):
    return [int(bit) for char in message for bit in format(ord(char), '08b')]

def bits_to_string(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(''.join(map(str, byte)), 2)) for byte in chars)

def generate_subkeys(key):
    key = permute(key, pc1_table)
    C, D = key[:28], key[28:]
    subkeys = []
    for shift in shift_schedule:
        C = C[shift:] + C[:shift]
        D = D[shift:] + D[:shift]
        subkeys.append(permute(C + D, pc2_table))
    return subkeys

def feistel(R, subkey):
    expanded_R = permute(R, e)
    xor_result = xor(expanded_R, subkey)
    substituted = []
    for i in range(8):
        block = xor_result[i*6:(i+1)*6]
        row = (block[0] << 1) | block[5]
        col = int(''.join(map(str, block[1:5])), 2)
        value = S_boxes[i][row][col]
        substituted.extend(format(value, '04b'))
    return permute([int(bit) for bit in substituted], p)

def des_encrypt_block(block, subkeys):
    block = permute(block, ip_table)
    L, R = block[:32], block[32:]
    for i in range(16):
        new_R = xor(L, feistel(R, subkeys[i]))
        L, R = R, new_R
    return permute(R + L, ip_inverse)

def des_decrypt_block(block, subkeys):
    block = permute(block, ip_table)
    L, R = block[:32], block[32:]
    for i in reversed(range(16)):
        new_L = xor(R, feistel(L, subkeys[i]))
        R, L = L, new_L
    return permute(R + L, ip_inverse)

def pad_text(bits):
    padding_length = 64 - (len(bits) % 64)
    return bits + [0] * padding_length

def unpad_text(bits):
    return bits[:len(bits) - bits[::-1].index(1)] if 1 in bits else bits

def des_encrypt(text, key):
    if isinstance(text, int):  # Se for um inteiro, converta para string
        text = str(text)
    if isinstance(key, int):  # Se for um inteiro, converta para string
        key = str(key)
    
    key_bits = string_to_bits(key)[:64]  # Aqui a chave será corretamente convertida para bits
    subkeys = generate_subkeys(key_bits)
    text_bits = pad_text(string_to_bits(text))  # Certifique-se de que text é uma string
    encrypted_bits = []
    
    for i in range(0, len(text_bits), 64):
        block = text_bits[i:i+64]
        encrypted_bits.extend(des_encrypt_block(block, subkeys))
    
    return encrypted_bits

def des_decrypt(encrypted_bits, key):
    key_bits = string_to_bits(key)[:64]
    subkeys = generate_subkeys(key_bits)
    decrypted_bits = []
    for i in range(0, len(encrypted_bits), 64):
        block = encrypted_bits[i:i+64]
        decrypted_bits.extend(des_decrypt_block(block, subkeys))
    return bits_to_string(unpad_text(decrypted_bits))