#!/usr/bin/env python3
from sqlite3ctrl import DataBase
from dbcrypt import Password
from functions import *
import argparse
import os


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
    # create random string
    rand_str = random_string_generate()
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
            # create password object
            passwd = Password()
            passwd.setup()
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
            # create password object
            passwd = Password()
            passwd.setup()
            print(db1.delete_row({"id": row_id}))
        except UnboundLocalError:
            print("Please set row id with --id")
    if args.insert:
        try:
            # create password object
            passwd = Password()
            passwd.setup()
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
        # create password object
        passwd = Password()
        passwd.setup()
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
    if args.show_content:
        # create password object
        passwd = Password()
        passwd.setup()
        print(db1.show_fancy_table(passwd.dec_list_of_tuples(
            db1.show_table_content())))
    if args.show_enc_content:
        for row in db1.show_normal_row(db1.show_table_content()):
            print(row)

if __name__ == "__main__":
    main()
