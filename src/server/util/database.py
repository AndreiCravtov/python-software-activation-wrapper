import json
import crypto as crp
import keygen as kgn

DATABASE_FILE_PATH = 'data/licence/licencedatabase.txt'

class LicenceDatabaseUtils:
    @staticmethod
    def check_if_valid_and_fix_if_not(path=DATABASE_FILE_PATH):
        try:
            file = open(path, 'r', encoding=crp.ENCODING_STANDARD)
            data = json.loads(file.read(), strict=False)

            # perform validity checks on data file
            if not ('active_keys' in data and 'used_keys' in data):
                raise Exception("Database file corrupted")
            else:
                if not (type(data['active_keys']) is list and
                        type(data['used_keys']) is list):
                    raise Exception("Database file corrupted")

            file.close()

        except Exception as e:
            print("Some exception: "+str(e))
            file = open(path, 'w', encoding=crp.ENCODING_STANDARD)

            data = {
                'active_keys': [],
                'used_keys': []
            }

            file.write(json.dumps(data))
            file.close()

    @staticmethod
    def check_key_checksum_validity(key, checksum):
        # check for key/checksum validity
        if not (checksum == kgn.KeyUtils.get_key_checksum(key) and 
                kgn.ServerKeyUtils.validate_key(key)):
            raise Exception("Invalid key or checksum")

    @staticmethod
    def add_active_key(key, checksum, path=DATABASE_FILE_PATH):
        LicenceDatabaseUtils.check_if_valid_and_fix_if_not()

        # check for key/checksum validity
        LicenceDatabaseUtils.check_key_checksum_validity(key, checksum)

        data_text = open(path, 'r', encoding=crp.ENCODING_STANDARD).read()
        data = json.loads(data_text, strict=False)

        data['active_keys'].append(
            {
                'key': key,
                'checksum': checksum
            }
        )

        open(path, 'w', encoding=crp.ENCODING_STANDARD).write(json.dumps(data))

    @staticmethod
    def remove_active_key(key, checksum, path=DATABASE_FILE_PATH):
        LicenceDatabaseUtils.check_if_valid_and_fix_if_not()

        # check for key/checksum validity
        LicenceDatabaseUtils.check_key_checksum_validity(key, checksum)

        data_text = open(path, 'r', encoding=crp.ENCODING_STANDARD).read()
        data = json.loads(data_text, strict=False)

        # search for the entry
        search_result = {
            'found': False,
            'index': -1
        }
        for i in range(len(data['active_keys'])):
            if key == data['active_keys'][i]['key'] and checksum == data['active_keys'][i]['checksum']:
                search_result['found'] = True
                search_result['index'] = i

        # delete entry if exists
        if search_result['found']:
            del data['active_keys'][search_result['index']]

        open(path, 'w', encoding=crp.ENCODING_STANDARD).write(json.dumps(data))

    @staticmethod
    def add_used_key(key, checksum, path=DATABASE_FILE_PATH):
        LicenceDatabaseUtils.check_if_valid_and_fix_if_not()

        # check for key/checksum validity
        LicenceDatabaseUtils.check_key_checksum_validity(key, checksum)

        data_text = open(path, 'r', encoding=crp.ENCODING_STANDARD).read()
        data = json.loads(data_text, strict=False)

        data['used_keys'].append(
            {
                'key': key,
                'checksum': checksum
            }
        )

        open(path, 'w', encoding=crp.ENCODING_STANDARD).write(json.dumps(data))

    @staticmethod
    def remove_used_key(key, checksum, path=DATABASE_FILE_PATH):
        LicenceDatabaseUtils.check_if_valid_and_fix_if_not()

        # check for key/checksum validity
        LicenceDatabaseUtils.check_key_checksum_validity(key, checksum)

        data_text = open(path, 'r', encoding=crp.ENCODING_STANDARD).read()
        data = json.loads(data_text, strict=False)

        # search for the entry
        search_result = {
            'found': False,
            'index': -1
        }
        for i in range(len(data['used_keys'])):
            if key == data['used_keys'][i]['key'] and checksum == data['used_keys'][i]['checksum']:
                search_result['found'] = True
                search_result['index'] = i

        # delete entry if exists
        if search_result['found']:
            del data['used_keys'][search_result['index']]

        open(path, 'w', encoding=crp.ENCODING_STANDARD).write(json.dumps(data))

    @staticmethod
    def check_checksum(checksum, path=DATABASE_FILE_PATH):
        LicenceDatabaseUtils.check_if_valid_and_fix_if_not()

        data_text = open(path, 'r', encoding=crp.ENCODING_STANDARD).read()
        data = json.loads(data_text, strict=False)

        # if checksum exists return true
        for i in range(len(data['active_keys'])):
            if checksum == data['active_keys'][i]['checksum']:
                return True

        # else return false
        return False

if __name__ == "__main__": # check if this is code is being executed from the source file
    raise Exception("This is a module. Import it to use...") # if yes, throw an error