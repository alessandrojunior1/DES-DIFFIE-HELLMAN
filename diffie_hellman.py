import util

class DiffieHellman:
    def __init__(self, p=23, g=5):
        self.p = p
        self.g = g
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key()

    def generate_public_key(self):
        return (self.g ** self.private_key) % self.p
    
    def generate_private_key(self):
        return util.random_number_prime(1, 50)

    def generate_shared_key(self, received_public):
        return (received_public ** self.private_key) % self.p
