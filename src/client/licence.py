import crypto as crp
import keygen as kgn
import servercom as scm

import uuid
import json

LICENCE_FILE_PATH = './data/activation/software_licence.txt'

class SoftwareLicence:
    @staticmethod
    def activate_software(licence_key):
        try:
            # return False if client finds the key to be invalid
            if not kgn.ClientKeyUtils.validate_key(licence_key):
                return False

            # initialise server communication
            server_communication = scm.ServerCommunication()

            # return False if couldn't connect to server
            if not server_communication.connected:
                return False

            # generate unique machine id hash
            unique_machine_id_hash = crp.CryptoUtils.sha256_hash(str(uuid.getnode()))

            # send main data
            server_communication.send_message({
                "message": {
                    "encrypted_key": crp.CryptoUtils.rsa_encrypt(licence_key), # encrypted valid key
                    "checksum": kgn.KeyUtils.get_key_checksum(licence_key), # first 4 bytes of the hash of the valid key
                    "unique_machine_id_hash": unique_machine_id_hash # hash of unique machine id
                }
            })

            # get return data
            message = server_communication.receive_message()
            payload = message["message"] if "message" in message else {}

            # close connection
            server_communication.close_connection()

            # return False if sent data doesn't have the stamp, certificate and their signatures
            if not (isinstance(payload, dict) and 
                "stamp" in payload and isinstance(payload["stamp"], dict) and
                    "stamp" in payload["stamp"] and isinstance(payload["stamp"]["stamp"], str) and
                    "stamp_signature" in payload["stamp"] and isinstance(payload["stamp"]["stamp_signature"], str) and
                "certificate" in payload and isinstance(payload["certificate"], dict) and
                    "certificate" in payload["certificate"] and isinstance(payload["certificate"]["certificate"], str) and
                    "certificate_signature" in payload["certificate"] and isinstance(payload["certificate"]["certificate_signature"], str)):
                return False

            # return False if received server data is invalid for whatever reason 
            if not (
                crp.CryptoUtils.rsa_verify(payload["stamp"]["stamp_signature"], payload["stamp"]["stamp"]) and
                crp.CryptoUtils.rsa_verify(payload["certificate"]["certificate_signature"], payload["certificate"]["certificate"]) and
                payload["certificate"]["certificate"] == crp.CryptoUtils.sha256_hash(licence_key + payload["stamp"]["stamp"] + unique_machine_id_hash)):
                return False

            # create a licence key file
            SoftwareLicence.generate_licence_file(licence_key, payload)

            # double check file validity
            if not SoftwareLicence.validate_licence_file():
                # return False if for whatever reason the file is invalid
                return False

            # if successful then return True
            return True

        except Exception as e:
            print(e)

            # return False if an unhandled exception occurs
            return False

    @staticmethod
    def generate_licence_file(key, server_data, file_path=LICENCE_FILE_PATH):

        # create a storage dictionary
        storage_data = server_data; storage_data["key"] = key

        # create a json string and encrypt it
        encrypted_json = crp.CryptoUtils.acc_encrypt(json.dumps(storage_data))
        
        # save licence data
        open(file_path, 'w', encoding=crp.ENCODING_STANDARD).write(encrypted_json)

    @staticmethod
    def validate_licence_file(file_path=LICENCE_FILE_PATH):
        try:
            # read licence data
            encrypted_json = open(file_path, 'r', encoding=crp.ENCODING_STANDARD).read()
            decrypted_json = crp.CryptoUtils.acc_decrypt(encrypted_json)
            storage_data = json.loads(decrypted_json)
        
            # verify key validity
            key = storage_data['key']
            if not kgn.ClientKeyUtils.validate_key(key, kgn.ALPHABET):
                return False
            
            # verify stamp validity
            stamp = storage_data['stamp']['stamp']
            stamp_signature = storage_data['stamp']['stamp_signature']
            if not crp.CryptoUtils.rsa_verify(stamp_signature, stamp):
                print("Stamp not valid")
                return False
            
            # generate in-house unique machine id hash
            unique_machine_id_hash = crp.CryptoUtils.sha256_hash(str(uuid.getnode()))

            # verify certificate validity
            stored_certificate = storage_data['certificate']['certificate']
            stored_certificate_signature = storage_data['certificate']['certificate_signature']
            if not crp.CryptoUtils.rsa_verify(stored_certificate_signature, stored_certificate):
                print("Stored certificate not valid")
                return False

            # generate in-house certificate
            generated_certificate = crp.CryptoUtils.sha256_hash( key + stamp + unique_machine_id_hash )

            # check if generated certificate matches stored certificate
            if not generated_certificate == stored_certificate:
                print("Certificate not valid")
                return False
        except Exception as e:
            print(e)
            return False
        return True

if __name__ == "__main__": # check if this is code is being executed from the source file
    raise Exception("This is a module. Import it to use...") # if yes, throw an error