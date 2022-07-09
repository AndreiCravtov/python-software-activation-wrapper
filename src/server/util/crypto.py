import hashlib
import rsa

# Define some public variables
ENCODING_STANDARD = 'latin1'
PUBLIC_KEY = rsa.PublicKey.load_pkcs1(open('./data/keys/public_key.txt', 'r').read().encode(ENCODING_STANDARD))
PRIVATE_KEY = rsa.PrivateKey.load_pkcs1(open('./data/keys/private_key.txt', 'r').read().encode(ENCODING_STANDARD))

class CryptoUtils:

    @staticmethod
    def sha256_hash(message, encoding_standard=ENCODING_STANDARD):
        """Returns a SHA256 digest of any given input as text"""
        digest = hashlib.sha256(message.encode(encoding_standard)).digest().decode(encoding_standard)
        
        return digest

    @staticmethod
    def generate_random_rsa_keyair(bit_number, encoding_standard=ENCODING_STANDARD):
        """Generates a random RSA keypair in the PKCS#1 PEM standard as text"""
        (public_key, private_key) = rsa.newkeys(bit_number)

        return public_key._save_pkcs1_pem().decode(encoding_standard), private_key._save_pkcs1_pem().decode(encoding_standard)

    @staticmethod
    def rsa_encrypt(plaintext, public_key=PUBLIC_KEY, encoding_standard=ENCODING_STANDARD):
        """Returns encrypted ciphertext given a key as text"""

        try:
            return rsa.encrypt(plaintext.encode(encoding_standard), public_key).decode(encoding_standard)
        except:
            return
    
    @staticmethod
    def rsa_decrypt(ciphertext, private_key=PRIVATE_KEY, encoding_standard=ENCODING_STANDARD):
        """Returns decrypted plaintext given a key as text"""

        try:
            return rsa.decrypt(ciphertext.encode(encoding_standard), private_key).decode(encoding_standard)
        except:
            return

    @staticmethod
    def rsa_sign(message, private_key=PRIVATE_KEY, encoding_standard=ENCODING_STANDARD):
        """Generates a signature for a given message as text"""

        try:
            return rsa.sign(message.encode(encoding_standard), private_key, 'SHA-256').decode(encoding_standard)
        except:
            return

    @staticmethod
    def rsa_verify(signature, message, public_key=PUBLIC_KEY, encoding_standard=ENCODING_STANDARD):
        """Verifies signature integrity for a given message"""

        try:
            if rsa.verify(message.encode(encoding_standard), signature.encode(encoding_standard), public_key) == 'SHA-256':
                return True
        except:
            pass
        
        return False

if __name__ == "__main__": #check if this is code is being executed from the source file
    raise Exception("This is a module. Import it to use...") #if yes, throw an error