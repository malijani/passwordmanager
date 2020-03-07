#!/usr/bin/env python3
import sqlite3
from prettytable import PrettyTable
# module to control sqlite3 database
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
