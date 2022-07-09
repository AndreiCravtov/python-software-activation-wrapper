import crypto as crp

import random
import hashlib

# Shared ALPHABET variable
ALPHABET = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# Server SEED variable
SEED = '22712740814523114'

class KeyUtils:
    """A base class that provides some serial key utility"""

    @staticmethod
    def random_float(seed, start, end):
        """Generates a random float from a seed and a range"""

        # Hash the object and obtain an integer representation of the hash
        hashed_object = hashlib.sha256(bytes(seed, encoding='utf8'))
        hash_number = int.from_bytes(hashed_object.digest(), byteorder='big', signed=False)

        # Generate a decimal from 0 to 1 using the previously generated number
        random_decimal = (hash_number)/(2**256)
        random_number = random_decimal*(end-start)+start

        return random_number

    @staticmethod
    def random_int(seed, start, end):
        """Generates a random int from a seed and a range"""
        
        return int(KeyUtils.random_float(seed, start, end))

    @staticmethod
    def random_choice(seed, choice_list):
        """Picks random item from a list"""
        
        return choice_list[KeyUtils.random_int(seed, 0, len(choice_list)-1)]

    @staticmethod
    def get_key_checksum(key):
        return crp.CryptoUtils.sha256_hash(crp.CryptoUtils.sha256_hash(key))[:4]

class ClientKeyUtils:
    """A client class that handles limited verification and utility"""

    @staticmethod
    def validate_key(key, alphabet=ALPHABET):
        """Verifies whether or not a serial key is valid using the hash check"""

        # Check key length is (25) charecters
        if len(key) != 25:
            return False

        # Check if only valid charecters are used
        if not set(key).issubset(set(alphabet)):
            return False

        # Check if the first (3) digits of the hash of the key is (3) pseudorandomly generated hex charecters
        key_hash = hashlib.sha256(bytes(key, encoding='utf8')).hexdigest()
        if key_hash[:3] != ''.join([KeyUtils.random_choice(key_hash+str(i), '0123456789abcdef') for i in range(3)]):
            return False
                
        return True

class ServerKeyUtils:
    """A server class that handles all key generation and verification and utility"""
    
    @staticmethod
    def validate_key(key, seed=SEED, alphabet=ALPHABET):
        """Verifies whether or not a serial key is valid using the server variable SEED and the hash check"""

        # Check if client validation is passed
        if not ClientKeyUtils.validate_key(key, alphabet):
            return False

        # Creates a list of (4) charecters derrived from SEED and key
        included_charecter_list = []
        iterator=0
        while len(included_charecter_list) < 4:
            unique_seed = str(iterator) + seed + key
            charecter = KeyUtils.random_choice(unique_seed, alphabet)
            included_charecter_list.append(charecter)
            included_charecter_list = list(set(included_charecter_list))
            iterator += 1 

        # Check if the key includes the list of charecters to be included
        if not set(included_charecter_list).issubset(set(key)):
            return False
                
        return True

    @staticmethod    
    def generate_key(seed=SEED, alphabet=ALPHABET):
        """Generates a server-valid key using the server variable SEED"""

        # Randomly generate keys until the key is valid
        while True:

            # Generate random key
            key = ''
            while len(key) < 25:
                key += random.choice(alphabet)

            # Check if the key is valid
            if ServerKeyUtils.validate_key(key, seed, alphabet):
                return key

if __name__ == "__main__": # check if this is code is being executed from the source file
    raise Exception("This is a module. Import it to use...") # if yes, throw an error