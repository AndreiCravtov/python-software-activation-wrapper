import crypto as crp
import keygen as kgn
import database as db
from copy import deepcopy as copy

class SoftwareLicence:

    @staticmethod
    def generate_licence_components(incoming_data):
        # pass by value instead of reference
        message = copy(incoming_data)

        # get decrypted object
        payload = SoftwareLicence.decrypt_key(message)["message"]

        # create stamp and it's signature
        stamp = crp.CryptoUtils.sha256_hash(payload["key"] + kgn.SEED)
        stamp_signature = crp.CryptoUtils.rsa_sign(stamp)

        # create certificate and it's signature
        certificate = crp.CryptoUtils.sha256_hash(payload["key"] + stamp + payload["unique_machine_id_hash"])
        certificate_signature = crp.CryptoUtils.rsa_sign(certificate)

        return {
            'stamp': {
                'stamp': stamp,
                'stamp_signature': stamp_signature
            },
            'certificate': {
                'certificate': certificate,
                'certificate_signature': certificate_signature
            }
        }

    @staticmethod
    def validate_incoming_licence_components(incoming_data):
        # pass by value instead of reference
        message = copy(incoming_data)

        # check that encrypted key, checksum and unique machine id are in the message and are strings
        payload = message["message"] if "message" in message else {}
        if not (isinstance(payload, dict) and 
            "encrypted_key" in payload and isinstance(payload["encrypted_key"], str) and
            "checksum" in payload and isinstance(payload["checksum"], str) and
            "unique_machine_id_hash" in payload and isinstance(payload["unique_machine_id_hash"], str)):
            return False

        # check if the checksum is valid
        if not db.LicenceDatabaseUtils.check_checksum(payload["checksum"]):
            return False

        # decrypt key
        payload = SoftwareLicence.decrypt_key(message)["message"]

        # check if the key is valid
        if not kgn.ServerKeyUtils.validate_key(payload["key"]):
            return False

        # check if checksum is valid
        generated_checksum = kgn.KeyUtils.get_key_checksum(payload["key"])
        if not (payload["checksum"] == generated_checksum):
            return False

        return True

    @staticmethod
    def decrypt_key(incoming_data):
        # pass by value instead of reference
        message = copy(incoming_data)

        # decrypt and get key
        encrypted_key = message["message"]["encrypted_key"]
        key = crp.CryptoUtils.rsa_decrypt(encrypted_key)

        # set to empty string if key decryption failed
        if key is None: key = ''

        # update object
        message["message"]["key"] = key; del message["message"]["encrypted_key"]

        return message

if __name__ == "__main__": # check if this is code is being executed from the source file
    raise Exception("This is a module. Import it to use...") # if yes, throw an error