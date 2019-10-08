#!/usr/bin/env python3
import sqlite3
import argparse
import base64
import os
import hashlib
import random
import string
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from prettytable import PrettyTable


# class to control sqlite3 database
class DataBase:
    # set database address , table name, fields of table in a list
    def __init__(self, database_address, table_name, fields: list):
        self.table_name = table_name
        self.fields = fields
        self.database_address = database_address

    # initialize connection and set self.cnx
    def connect_to_db(self):
        try:
            # connect to self.database_address
            cnx = sqlite3.connect(self.database_address)
            self.cnx = cnx
            return f"Connected to {self.database_address} successfully"
        except sqlite3.Error:
            return f"Error connecting to {self.database_address}"

    # initialize cursor to execute sql commands and set self.cursor
    def create_cursor(self):
        # set cusor by using connection
        cursor = self.cnx.cursor()
        self.cursor = cursor
        return f"Successfully created {self.cursor}"

    # return all of tables in database
    def show_tables(self):
        sql = '''SELECT name FROM sqlite_master WHERE type="table"'''
        self.cursor.execute(sql)
        tables = ""
        for tup in self.cursor.fetchall():
            for lst in tup:
                tables += f"{lst} "
        return f"'{tables.strip()}' exist in '{self.database_address}'"

    # check if table is already in database or not!
    # False for being in database and True if the table doesn't exist
    def check_table_existence(self):
        sql = f'''SELECT count(name) FROM sqlite_master WHERE type='table'
                AND name='{self.table_name}' '''
        self.cursor.execute(sql)
        # if matching table finded the self.cursor.fetchone()[0] equals to 1
        if self.cursor.fetchone()[0] == 1:
            return False
        else:
            return True

    # check if rowid exist in database
    def check_id_existence(self, data: dict):
        # join keys for setting fields {"field[0]": 'val', "field[1]": 'val'}
        column = ''.join(data.keys())
        # set a tuple of values to pass them in execute() method
        values = tuple(data.values())
        sql = f'''SELECT count(id) FROM {self.table_name} WHERE {column}=?'''
        self.cursor.execute(sql, values)
        data = self.cursor.fetchone()[0]
        if data == 0:
            return False
        else:
            return True

    # create table in database using self.check_table_existence()
    def create_table(self):
        if self.check_table_existence():
            sql = ""
            last_item = len(self.fields) - 1
            for field in self.fields:
                if field == self.fields[0]:
                    sql += f'''CREATE TABLE {self.table_name}
                    ({field} integer PRIMARY KEY,'''
                elif field == self.fields[last_item]:
                    sql += f" {field} text)"
                else:
                    sql += f" {field} text,"
            self.cursor.execute(sql)
            self.cnx.commit()
            return f"Successfully created {self.table_name}"
        else:
            return f"{self.table_name} table already exist in database!"

    # return all of table contents in a list of tuples
    def show_table_content(self):
        sql = f'''SELECT * FROM {self.table_name}'''
        try:
            self.cursor.execute(sql)
        except sqlite3.OperationalError:
            return f"Please create {self.table_name}"
        else:
            rows = self.cursor.fetchall()
            return rows

    # search in table with custom dictionary of {field: val}
    def search_in_table(self, data: dict):
        if self.check_id_existence(data):
            # join keys for setting fields {"field[0]": 'val',..}
            column = ''.join(data.keys())
            # set a tuple of values to pass them in execute() method
            values = tuple(data.values())
            sql = f'''SELECT * FROM {self.table_name} WHERE {column}=?'''
            try:
                self.cursor.execute(sql, values)
            except sqlite3.OperationalError:
                return f'''Error: Please set correct data to search as your fields :
             {self.fields}'''
            rows = self.cursor.fetchall()
            if rows == []:
                return f"There's not any row matches : {data}"
            else:
                return rows
        else:
            return f"There's not any row exist with {data}"

    # add data into table with a tuple of field values
    def insert_into_table(self, values: tuple):
        # set string of fields to use them in sql query
        sql_fields = ""
        # set string for ? marks in sql query
        values_mark = ""
        # find last_item index to set as end of line
        last_item = len(self.fields) - 1
        for field in self.fields:
            # don't mess with 'id' field
            if field == self.fields[0]:
                pass
            # set query style of last field
            elif field == self.fields[last_item]:
                sql_fields += f"{field}"
                values_mark += "?"
            # set query style of normal fields with ','
            else:
                sql_fields += f"{field},"
                values_mark += "?,"
        sql = f'''INSERT INTO {self.table_name}({sql_fields})
            VALUES({values_mark})'''
        try:
            self.cursor.execute(sql, values)
        except (sqlite3.ProgrammingError, sqlite3.OperationalError):
            return f"""Please set values as your fields: {self.fields}
        and existence of {self.table_name} table"""
        self.cnx.commit()
        return f"Created new row id: {self.cursor.lastrowid}"

    # change data in a specific row of table
    # by setting id and another field to change
    # {"id":1, "field": "new_data", "another_field": "another_new_data"}
    def update_db_content(self, data: dict):
        # if self.check_id_existence(data):
        # set id row to change data in it
        where = data.pop('id')
        # set query for fields of table by joining keys
        columns = '=?, '.join(data.keys()) + '=?'
        # set a tuple of values to change them
        values = tuple(data.values()) + (where,)
        sql = f'''UPDATE {self.table_name} SET {columns}
        WHERE {self.fields[0]}=?'''
        self.cursor.execute(sql, values)
        self.cnx.commit()
        return f"Updated row {values[-1]}"
        # else:
        #    return f"There's not any row to update with : {data}"

    # delete a row with id : {"id": 1}
    def delete_row(self, data: dict):
        if self.check_id_existence(data):
            # set row id: that's just one value to set! so we need tuple: (1,)
            where = tuple([data.pop('id')])
            sql = f'''DELETE FROM {self.table_name} WHERE {self.fields[0]}=?'''
            self.cursor.execute(sql, where)
            self.cnx.commit()
            return f"Deleted row {where[-1]} in {self.table_name}"
        else:
            return f"There's not any row to delete with : {data}"

    # method to return all datas of a row in fancy way using PrettyTable()
    # for 'JUST' printing situations
    def show_fancy_table(self, list_of_tuples):
        # create object from PrettyTable()
        x = PrettyTable()
        # set fields of table
        x.field_names = self.fields
        # add rows of table to PrettyTable method: add_row()
        for row in list_of_tuples:
            x.add_row(row)
        return x

    # shows output of a row more normal
    def show_normal_row(self, list_of_tuples):
        for tup in list_of_tuples:
            row_dict = {}
            count = 0
            for value in tup:
                row_dict.update({f"{self.fields[count]}": f"{value}"})
                count += 1
            yield "{" + "\n".join("{}: {}".format(k, v)
                                  for k, v in row_dict.items()) + "}"

    # magick method to return everything from database object
    def __str__(self):
        status = f"""Database info:
                \r\taddress: {self.database_address}
                \r\tusing table: {self.table_name}
                \r\tusing fields: {self.fields}"""
        try:
            status += f'''\n\r\tall tables: {self.show_tables()}
                \r\tcursor: {self.cursor}
                \r\tconnection: {self.cnx}'''
            return status.strip()
        except AttributeError:
            return "Please connect to database and create cursor!"

    def __del__(self):
        try:
            self.cnx.close()
        except AttributeError:
            return "Connection doesn't exist!"


class Password:
    def __init__(self):
        self.custom_string = input("(KEY):> ").encode()

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

    def enc(self, string: str):
        string = str(string)
        return self.f.encrypt(string.encode()).decode()

    def dec(self, enc_string: str):
        try:
            enc_string = str(enc_string)
            return self.f.decrypt(enc_string.encode()).decode()
        except:
            return "Invalid Signature"

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
    custom_chars = ["!", "@", "#", "$", "%", "_", "+", "*", "[",
                    "]", "(", ")", "=", "&", "?", ":", ".", "-",
                    "^", "A", "B", "C", "D", "E", "F", "G", "H",
                    "I", "J", "K", "L", "M", "N", "O", "P", "Q",
                    "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    custom_key = ''.join(random.choice(custom_chars) for x in range(10))
    password = sha512 + custom_key
    shuffle_password = ''.join(random.sample(password, len(password)))
    return shuffle_password


# main code
def main():
    parser = argparse.ArgumentParser(prog='PASS STORE',
                                     description='''passwordmanager is a
                                     programm to manage password database''')
    parser.add_argument("--id",
                        help='''table id for process''',
                        type=int)

    parser.add_argument("--user_name",
                        help="set user name")

    parser.add_argument("--website_address",
                        help='''websiteaddress''')

    parser.add_argument("--phone_number",
                        help="set phone number")

    parser.add_argument("--password",
                        help='''user "GEN" to generate password
                        or set your custom password or "SHOW" to show generated password''')

    parser.add_argument("--length",
                        help='''set password length for auto-generation''',
                        type=int)

    #parser.add_argument("--intractive",
                        #help="take data in intractive mode",
                        #action="store_true")

    parser.add_argument("--email",
                        help="set acc email")

    parser.add_argument("--description",
                        help="set field description")

    parser.add_argument("--delete",
                        help="delete a specific row",
                        action="store_true")

    parser.add_argument("--update",
                        help="change data in row",
                        action="store_true")

    parser.add_argument("--show_content",
                        help="show table",
                        action="store_true")

    parser.add_argument("--show_enc_content",
                        help="show enc table",
                        action="store_true")

    parser.add_argument("--insert",
                        help="create a new row",
                        action="store_true")

    parser.add_argument("--table_name",
                        help="table name")

    parser.add_argument("--database",
                        help="database address")

    parser.add_argument("--get_tables",
                        help='''get tablenames in database''',
                        action="store_true")

    parser.add_argument("--search",
                        help="search in table with website address")

    args = parser.parse_args()

    table_name = "encrypted_data"
    database = "passwords.db"
    db1_fields = ["id",
                  "website_address",
                  "user_name",
                  "password",
                  "email",
                  "phone_number",
                  "description"
                  ]
    if args.database:
        database = args.database
    if args.table_name:
        table_name = args.table_name
    # create database object
    db1 = DataBase(
        database,
        table_name,
        db1_fields
    )
    # connect to database
    db1.connect_to_db()
    # create cursor
    db1.create_cursor()
    # create table
    db1.create_table()
    # create password object
    passwd = Password()
    passwd.setup()
    # create random string
    rand_str = random_string_generate()
    if args.show_content:
        print(db1.show_fancy_table(passwd.dec_list_of_tuples(
            db1.show_table_content())))
    if args.show_enc_content:
        for row in db1.show_normal_row(db1.show_table_content()):
            print(row)
    if args.get_tables:
        print(db1.show_tables())
    if args.id:
        row_id = args.id
    else:
        row_id = None
    if args.website_address:
        website_address = args.website_address
    else:
        website_address = None
    if args.user_name:
        user_name = args.user_name
    else:
        user_name = None
    if args.length:
        length = args.length
    else:
        length = 20
    if args.password:
        password = args.password
        if password.lower() == "gen":
            try:
                password = create_password(website_address, user_name,
                                           rand_str, length)
            except UnboundLocalError:
                print('''Please set WEBSITE_ADDRESS USER_NAME
                       (LENGTH is optional)''')
        elif password.lower() == "show":
            try:
                print(create_password(website_address, user_name,
                                      rand_str, length))
            except UnboundLocalError:
                print('''Please set WEBSITE_ADDRESS USER_NAME
                       (LENGTH is optional)''')
    else:
        password = None
    if args.email:
        email = args.email
    else:
        email = None
    if args.phone_number:
        phone_number = args.phone_number
    else:
        phone_number = None
    if args.description:
        description = args.description
    else:
        description = None
    if args.table_name:
        table = args.table_name
    if args.database:
        database = args.database
    #if args.intractive:
        #pass
    if args.update:
        try:
            data = {"id": row_id,
                    "website_address": website_address,
                    "user_name": user_name,
                    "password": password,
                    "email": email,
                    "phone_number": phone_number,
                    "description": description}
            correct_data = fix_update_dictionary(data, passwd)
            print(db1.update_db_content(correct_data))
        except UnboundLocalError:
            print('''Please set ID and one other thing: WEBSITE_ADDRESS
                   USER_NAME PASSWORD EMAIL DESCRIPTION''')
    if args.delete:
        try:
            print(db1.delete_row({"id": row_id}))
        except UnboundLocalError:
            print("Please set row id with --id")
    if args.insert:
        try:
            print(db1.insert_into_table(
                           (passwd.enc(website_address),
                            passwd.enc(user_name),
                            passwd.enc(password),
                            passwd.enc(email),
                            passwd.enc(phone_number),
                            passwd.enc(description))))
        except UnboundLocalError:
            print('''Please set WEBSITE_ADDRESS USER_NAME
                   PASSWORD EMAIL PHONE_NUMBER DESCRIPTION''')
    if args.search:
        tb_content = db1.show_table_content()
        tb_dec_content = passwd.dec_list_of_tuples(tb_content)
        find_list = []
        for tup in tb_dec_content:
            if args.search in tup:
                find_list.append(tup)
        if len(find_list) == 0:
            print(f"Didn't find {args.search} in any row of {db1.table_name}")
        else:
            print(db1.show_fancy_table(find_list))

if __name__ == "__main__":
    main()
