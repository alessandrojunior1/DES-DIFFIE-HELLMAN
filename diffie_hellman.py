import util

class DiffieHellman:
    def __init__(self, g, p) -> None:
        self.__g = g
        self.__p = p
        self.__private_key = self.__generate_private_key()
        self.public_key = self.__generate_public_key()
        
    def __generate_private_key(self):
        return util.random_number_prime(2, 33333)
    
    def __generate_public_key(self):
        return (self.__g**self.__private_key) % self.__p
    
    def generate_shared_key(self, public_key_other):
        return (public_key_other**self.__private_key) % self.__p
        