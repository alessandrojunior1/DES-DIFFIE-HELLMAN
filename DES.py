class DES:
    def __init__(self, key: bytes):
        self.key = self.prepare_key(key)
        
    def ascii_to_binary(self, data: bytes):
        return ''.join(f'{ord(c):08b}' for c in data)
    
    def binary_to_ascii(self, data: str) -> str:
        return ''.join(chr(int(data[i:i+8], 2)) for i in range(0, len(data), 8))

    def prepare_key(self, key: bytes):
        """Converte a chave para 64 bits, removendo bits de paridade."""
        key_bin = self.ascii_to_binary(key)  # Converte a chave para binário
        if len(key_bin) < 64:
            key_bin = self.add_padding(key_bin)
        key_bin = key_bin[:64]  # Limita a 64 bits
        return key_bin

    def prepare_message(self, message):
        """Converte a mensagem para binário e adiciona padding."""
        message_bin = self.ascii_to_binary(message)
        blocks = [message_bin[i:i+64] for i in range(0, len(message_bin), 64)]
        if len(blocks[-1]) < 64:
            blocks[-1] = self.add_padding(blocks[-1])  # Corrige o último bloco
        return blocks  # Retorna os blocos corretamente


    def permute(self, data: str, table: list) -> str:
        """Permuta os bits de acordo com a tabela fornecida."""
        return ''.join(data[i-1] for i in table)

    def generate_subkeys(self):
        """Gera as 16 subchaves para cada rodada."""
        if not self.key:
            raise ValueError("Chave não definida.")
        #assert len(self.key) == 64, f"Chave tem tamanho errado: {len(self.key)} bits"
        key_bin = self.permute(self.key, self.__PC1)
        C, D = key_bin[:28], key_bin[28:]
        subkeys = []
        for shift in self.__SHIFTS:
            C, D = self.left_shift(C, shift), self.left_shift(D, shift)
            cd_combined = C + D
            subkey = self.permute(cd_combined, self.__PC2)
            subkeys.append(subkey)
        return subkeys

    def add_padding(self, bin) -> bytes:
        """Adiciona padding para garantir que a mensagem tenha 64 bits múltiplos."""
        if len(bin) < 64:
            bin += '0' * (64 - len(bin))
        return bin

    def feistel(self, L, R, subkey):
        """Função Feistel com expansão, XOR, S-Box e permutação."""
        expanded_R = self.permute(R, self.__EXPANSION)
        xored = ''.join('1' if expanded_R[i] != subkey[i] else '0' for i in range(48))
        substituted = self.s_box_substitution(xored)
        permuted = self.permute(substituted, self.__P)
        new_R = ''.join('1' if permuted[i] != L[i] else '0' for i in range(32))
        return R, new_R

    def xor(self, a, b):
        return ''.join('1' if a != y else '0' for x, y in zip(a, b))

    def split_blocks(self, block):
        return block[:32], block[32:]

    def hex_to_bin(self, hex_str):
       decimal_value = int(hex_str, 16)
       bin_value = bin(decimal_value)[2:]
       return bin_value.zfill(len(hex_str) * 4)
    
    def bin_to_hex(self, bin_str):
        decimal = int(bin_str, 2)
        hex_str = hex(decimal)[2:]
        return '0' * (len(bin_str) % 4) + hex_str

    def left_shift(self, key_part, shifts):
        return key_part[shifts:] + key_part[:shifts]

    def inital_permutation(self, block):
        return self.permute(block, self.__IP)

    def inverse_permutation(self, block):
        return self.permute(block, self.__IP_INVERSE)

    def s_box_substitution(self, data):
        """Aplica as S-Boxes para transformar 48 bits em 32 bits."""
        output = ''
        for i in range(8):
            block = data[i*6:(i+1)*6]
            row = int(block[0] + block[-1], 2)
            col = int(block[1:5], 2)
            output += format(self.__S_BOX[i][row][col], '04b')
        return output
    
    def encrypt(self, plaintext: bytes) -> bytes:
        """Criptografa um bloco de 64 bits."""
        blocks = self.prepare_message(plaintext)
        subkeys = self.generate_subkeys()
        ciphertext = ''
        for block in blocks:
            block = self.inital_permutation(block)
            L, R = self.split_blocks(block)
            for subkey in subkeys:
               L, R = self.feistel(L, R, subkey)
            combined_block = R + L
            ciphertext += self.inverse_permutation(combined_block)
        return self.bin_to_hex(ciphertext)
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        """Descriptografa um bloco de 64 bits."""
        blocks = self.hex_to_bin(ciphertext)
        blocks = [blocks[i:i+64] for i in range(0, len(blocks), 64)]
        subkeys = self.generate_subkeys()[::-1]
        plaintext = ''
        for block in blocks:
            block = self.inital_permutation(block)
            L, R = self.split_blocks(block)
            for subkey in subkeys:
                L, R = self.feistel(L, R, subkey)
            combined_block = R + L
            plaintext += self.inverse_permutation(combined_block)
        # if len(plaintext) % 8 != 0:
        #     plaintext = plaintext.zfill((len(plaintext) // 8 + 1) * 8)  # Ajusta o tamanho para múltiplo de 8
        return self.binary_to_ascii(plaintext)


    # Tabelas usadas pelo DES
    __IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
    ]

    __IP_INVERSE = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
    ]

    __PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
    ]

    __PC2 = [
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
    ]

    __SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    __EXPANSION = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
    ]

    __P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
    ]

    __S_BOX = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    ]