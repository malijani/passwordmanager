#!/usr/bin/env python3
# functions for main script
import string
import random
import hashlib

def fix_update_dictionary(data: dict, passwd):
    try:
        row_id_dict = {"id": data.pop("id")}
    except:
        return "Please set field id with --id"
    correct_data = dict([(k, passwd.enc(v))
                         for k, v in data.items()
                         if v is not None])
    all_data = {**row_id_dict, **correct_data}
    return all_data


def random_string_generate():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(10, 20)
    return ''.join(random.choice(chars) for x in range(size))


def create_password(address, user, random_string, length):
    complex_string = f"{address}_{random_string}_{user}"
    md5 = hashlib.md5(complex_string.encode('utf-8')).hexdigest()
    sha512 = f"{hashlib.sha512(md5.encode('utf-8')).hexdigest()[0:length-5]}"
    custom_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-',
                    '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^',
                    '_', '`', '{', '|', '}', '~', '!', '"', '#', '$', '%', '&', "'",
                    '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>',
                    '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    custom_key = ''.join(random.choice(custom_chars) for x in range(10))
    password = sha512 + custom_key
    if length :
        password = password[:length]
    shuffle_password = ''.join(random.sample(password, len(password)))
    return shuffle_password
