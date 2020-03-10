#!/usr/bin/env python3
# module to encrypt and decrypt data from sqlite3 database

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import getpass
import base64


class Password:
    def __init__(self):
        # get password : (This is a custom string that'll used for enc, dec)
        self.custom_string = getpass.getpass().encode()

    # set FERNET object
    def setup(self):
        salt = b'\x16\xf9\x84\xd0'
        # must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA1(),
            length=32,
            salt=salt,
            iterations=0,
            backend=default_backend()
        )
        # Can only use kdf once
        self.key = base64.urlsafe_b64encode(kdf.derive(self.custom_string))
        self.f = Fernet(self.key)

    def enc(self, string):
        # string to encrypt
        string = str(string)
        # encrypted string with f.encrypt()
        return self.f.encrypt(string.encode()).decode()


    def dec(self, enc_string):
        try:
            # string to encrypt
            enc_string = str(enc_string)
            # decrypt string with f.decrypt()
            return self.f.decrypt(enc_string.encode()).decode()
        except:
            return "Encrypted"

    def dec_list_of_tuples(self, list_of_tuples):
        list_of_rows = []
        for row in list_of_tuples:
            list_of_dec_rows = []
            row_list = list(row)
            for item in row_list:
                if item == row_list[0]:
                    list_of_dec_rows.append(item)
                    continue
                list_of_dec_rows.append(self.dec(item))
            row = tuple(list_of_dec_rows)
            list_of_rows.append(row)
        return list_of_rows
