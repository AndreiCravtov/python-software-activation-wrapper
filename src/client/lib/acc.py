# Advanced Caesar Cipher

import string, hashlib 

_CHUNK_SIZE = 64
_SHIFT_MAP = list(string.printable.replace('\r', '')) #create a map for shifting

def encrypt(msg, key):

    # check if message is valid
    if not (set(msg).issubset(set(_SHIFT_MAP))):
        return None
    
    shift_chain = [] 
    final = ""
    
    key = hashlib.sha256(bytes(key, 'utf-8')).hexdigest() # expand key into 64 charecters
    msg = _to_chunks(key+msg) # split the message into chunks and prepend the expanded key

    # loop through the amount of chunks the message was split into
    for i in range(len(msg)):
        # make a list of 64 integers for each chunk to shift each letter by
        # derived from the expanded key and the number of the chunk
        hash = hashlib.sha256(bytes(key + str(i), 'utf-8')).hexdigest()
        integer_array = _to_integer_array(hash)
        shift_chain.append(integer_array)
    for i in range(len(msg)): # loop through the amount of chunks the message was split into
        for j in range(len(msg[i])): # loop through each character of a chunk
            # shift the character by it's respective number
            # add it to final
            final += _shift(msg[i][j], shift_chain[i][j])
    return final # return final encrypted string

def decrypt(msg, key):

    # check if message is valid
    if not (set(msg).issubset(set(_SHIFT_MAP))):
        return None
    
    shift_chain = []
    final = ""
    
    key = hashlib.sha256(bytes(key, 'utf-8')).hexdigest() # expand key into 64 charecters
    msg = _to_chunks(msg) # split the message into chunks and prepend the expanded key

    # loop through the amount of chunks the message was split into
    for i in range(len(msg)):
        # make a list of 64 integers for each chunk to shift each letter by
        # derived from the expanded key and the number of the chunk
        hash = hashlib.sha256(bytes(key + str(i), 'utf-8')).hexdigest()
        integer_array = _to_integer_array(hash)
        shift_chain.append(integer_array)
    for i in range(len(msg)): # loop through the amount of chunks the message was split into
        for j in range(len(msg[i])): # loop through each character of a chunk
            # shift the character by it's respective number
            # add it to final
            final += _shift(msg[i][j], -shift_chain[i][j])
    if final[0:_CHUNK_SIZE] == key:
        # if the fist chunk of message is equal to the expanded key then the message is valid
        final = final.replace(key, '') # remove the expanded key
        return final # return final decrypted string
    else:
        return None

def _to_chunks(string, chunk_size=_CHUNK_SIZE): # define string to list with chunks converter
    if not string:
        return []
    
    chunks = [] # declare empty chunks list
    for i in range(len(string)): # loop through string and split it
        if i % chunk_size == 0:
            chunks.append('')
        chunks[i // chunk_size] += string[i]

    for i in range(len(chunks)): # loop through chunks list and turn strings into lists of charecters
        chunks[i] = list(chunks[i])
    
    return chunks

def _to_integer_array(string): # define character to it's ASCII number function
    return_value = [] # make a list
    for i in string: # go through each letter
        return_value.append(ord(i)) # add ASCII number of the current letter to list
    return return_value # return list

def _shift(char, num, char_map=_SHIFT_MAP): # define function to shift letters along a map by a given value
    index = ( char_map.index(char) + num ) % len(char_map) # find new index value
    return char_map[index] # return new shifted letter

if __name__ == "__main__": # check if this is code is being executed from the source file
    raise Exception("This is a module. Import it to use...") # if yes, throw an error