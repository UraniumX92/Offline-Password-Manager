import random
import json
import os

bullet_char = "\u2022"
user_data_file = "user_data.json"
passwords_file = "encrypted_passwords.json"


def generate_ascii_values():
    return [chr(num) for num in range(1,256)]

ascii_values = generate_ascii_values()


def random_KeyGen():
    return [random.randint(100,150) for x in range(9)]


def rng():
    return random.randint(0,6)


def key_mod(key:list,index:int,username:str):
    mod_key = key[1:-1]
    mod_key.insert(index,ord(username[0]))
    return mod_key


def ciph(text:str,key:list=None):
    if key is None:
        user_data = load_json(user_data_file)
        username = user_data['username']
        full_key = user_data['key']
        index = user_data['index']
        key = key_mod(key=full_key,index=index,username=username)

    ciphered_text = ''
    i = 0
    for charx in text:
        ascii_index = ord(charx)+key[i]
        if ascii_index >= len(ascii_values):
            ascii_index = ascii_index % len(ascii_values)
        elif ascii_index < 0:
            ascii_index = len(ascii_values) - (ascii_index*-1)
        ciphered_text += ascii_values[ascii_index-1]
        i += 1
        if i == len(key):
            i = 0
    return ciphered_text


def deciph(text:str,key:list=None):
    if key is None:
        user_data = load_json(user_data_file)
        username = user_data['username']
        full_key = user_data['key']
        index = user_data['index']
        key = key_mod(key=full_key,index=index,username=username)

    deciphered_text = ''
    i = 0
    for charx in text:
        ascii_index = ord(charx)-key[i]
        if ascii_index >= len(ascii_values):
            ascii_index = ascii_index % len(ascii_values)
        elif ascii_index < 0:
            ascii_index = len(ascii_values) - (ascii_index * -1)
        deciphered_text += ascii_values[ascii_index-1]
        i += 1
        if i == len(key):
            i = 0
    return deciphered_text


def dump_json(object,filename):
    with open(filename,"w") as dump:
        json.dump(object,dump,indent=4)


def load_json(filename):
    with open(filename,"r") as load:
        return json.load(load)


def check_and_create_file(filename,obj_type):
    if os.path.exists(os.path.join(os.getcwd(),filename)):
        try:
            if type(load_json(filename)) == type(obj_type):
                pass
        except:
            with open(filename,"w") as f:
                json.dump(obj_type,f)
    else:
        with open(filename,"w") as f:
            json.dump(obj_type,f)


def create_files():
    """
    Creates the Files using `check_and_create_file()` function
    """
    files_dict = {
        user_data_file : {'username':None},
        passwords_file : {'passwords':None}
    }
    for file,obj in files_dict.items():
        check_and_create_file(file,obj)


if __name__ == '__main__':
    key = random_KeyGen()
    print(key,len(key))
    print(key[1:-1])
    