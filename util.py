import random

def random_number(START=1,END=200):
    # Retorna um número aleatório entre um intervalo
    return random.randint(START,END)


def random_number_prime(START=1,END=200):
    # Retorna um número primo aleatório entre um intervalo
    while True:
        n = random.randint(START,END)
        if is_prime(n):
                return n

def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):  # 2 e 3 são primos
        return True
    if n % 2 == 0 or n % 3 == 0:  # Remove múltiplos de 2 e 3 rapidamente
        return False
    
    i = 5
    while i * i <= n:  # Testa apenas até √n
        if n % i == 0 or n % (i + 2) == 0:  # Testa i e i+2 (evita múltiplos de 2 e 3)
            return False
        i += 6  # Pula para o próximo possível divisor (6k ± 1)
    
    return True
