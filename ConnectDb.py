import os
import sqlite3

connname = 'phonebook.db'

class ConnectDb:
    def __init__(self, name_file='phonebook.db'):
        self.connstring = f'{name_file}'
        self.all_data = self.select_all_db()
        self.all_data_dict = self.from_sql_to_dict()
    
    def select_all_db(self):
        conn = sqlite3.connect(self.connstring)
        cursor = conn.cursor()
        data = cursor.execute('''SELECT * FROM PHONEBOOK''')
        cursor.close()
        conn.close()
        return data
    
    def clear_db(self):
        conn = sqlite3.connect(self.connstring)
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM PHONEBOOK;''')
        conn.commit()
        conn.close()
    
    def insert_in_db(self, id, lastname, firstname, phone, description):
        conn = sqlite3.connect(self.connstring)
        cursor = conn.cursor()
        dbstring = f'''INSERT INTO PHONEBOOK (ID, LASTNAME, FIRSTNAME, PHONE, DESCRIPTION) VALUES 
                ({id}, '{lastname}', '{firstname}', '{phone}', '{description}')'''
        cursor.execute(dbstring)
        conn.commit()
        conn.close()
    

    def from_sql_to_dict(self):
        conn = sqlite3.connect(self.connstring)
        cursor = conn.cursor()
        data = cursor.execute('''SELECT * FROM PHONEBOOK''')
        res = {}
        for id, row in enumerate(data):
            res[id] = {
                'lastname': row[1],
                'firstname': row[2],
                'phone': row[3],
                'description': row[4]
            }
        conn.close()
        return res

    def finish(self, data_dict):
        self.clear_db()
        for key, value in data_dict.items():
            self.insert_in_db(key, value["lastname"], value["firstname"], value["phone"], value["description"])