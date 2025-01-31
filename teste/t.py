from des import DES

# Chave fixa de 64 bits
key = b'12345678'
des = DES(key)

# Texto fixo de 8 bytes
mensagem_original = b"abc"

print("Texto original:", mensagem_original)

# Criptografar
encrypted = des.encrypt(mensagem_original)
print("Texto criptografado (binário):", ''.join(format(byte, '08b') for byte in encrypted))

# Descriptografar
decrypted = des.decrypt(encrypted)
print("Texto descriptografado:", decrypted)

# Verificar se a criptografia e a descriptografia são consistentes
if mensagem_original == decrypted:
    print("✅ Criptografia e descriptografia funcionando corretamente!")
else:
    print("❌ Erro: a mensagem descriptografada não corresponde à original!")
