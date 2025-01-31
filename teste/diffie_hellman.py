import random

class DiffieHellman:
    def __init__(self, p=23, g=5):
        self.p = p
        self.g = g
        self.private_key = random.randint(1, p - 1)

    def generate_public_key(self):
        return (self.g ** self.private_key) % self.p

    def generate_shared_key(self, received_public):
        return (received_public ** self.private_key) % self.p
