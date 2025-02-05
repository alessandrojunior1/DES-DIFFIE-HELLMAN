import random
import os

def random_number(s=1, e=100):
    """Gera um número aleatório dentro do intervalo, s(Start) e(End), especificado."""
    return random.randint(s, e)

def random_number_prime(s=2, e=100):
    """Gera um número primo aleatório dentro do intervalo, s(Start) e(End), especificado."""
    is_prime = lambda n: n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))
    while True:
        num = random_number(s, e)
        if is_prime(num):
            return num

def clear_terminal():
    """Limpa o terminal."""
    sistema = os.name
    if sistema == 'nt': #Para Windows
        os.system('cls')
    else: # Para Linux e outros sistemas(como macOS)
        os.system('clear')