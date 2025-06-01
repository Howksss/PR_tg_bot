import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(r'database/pnds.db')
        self.cursor = self.connection.cursor()
        self.connection.execute(
            '''CREATE TABLE IF NOT EXISTS pics (stage_name TEXT PRIMARY KEY,
                                                   content TEXT);'''
        )
        self.connection.execute(
            '''CREATE TABLE IF NOT EXISTS descs (stage_name TEXT PRIMARY KEY,
                                                   content TEXT);'''
        )

    def save_pic(self, content, stage_name):
        with self.connection:
            self.cursor.execute("UPDATE pics SET content=? WHERE stage_name=?", (content, stage_name))
            self.connection.commit()

    def delete_pic(self, stage_name):
        with self.connection:
            self.cursor.execute("DELETE FROM pics WHERE stage_name=?", (stage_name,))
            self.connection.commit()

    def save_desc(self, content, stage_name):
        with self.connection:
            self.cursor.execute("UPDATE descs SET content=? WHERE stage_name=?", (content, stage_name))
            self.connection.commit()

    def delete_desc(self, stage_name):
        with self.connection:
            self.cursor.execute("DELETE FROM descs WHERE stage_name=?", (stage_name,))
            self.connection.commit()

    def get_pic(self, stage_name):
        with self.connection:
            result = self.cursor.execute("SELECT content FROM pics WHERE stage_name=?", (stage_name,)).fetchone()
            result = result[0]
            self.connection.commit()
            return result
        
    def get_desc(self, stage_name):
        with self.connection:
            result = self.cursor.execute("SELECT content FROM descs WHERE stage_name=?", (stage_name,)).fetchone()
            result = result[0]
            self.connection.commit()
            return result
        
    def pic_exists(self, stage_name):
        with self.connection:
            result = self.cursor.execute("SELECT 1 FROM pics WHERE stage_name=?", (stage_name,)).fetchall()
            return bool(len(result))
        
    def desc_exists(self, stage_name):
        with self.connection:
            result = self.cursor.execute("SELECT 1 FROM descs WHERE stage_name=?", (stage_name,)).fetchall()
            return bool(len(result))
        

    def add_pic(self, stage_name, content):
        with self.connection:
            self.cursor.execute("REPLACE INTO pics ('stage_name','content') VALUES (?,?)", (stage_name, content))
            self.connection.commit()

    def add_desc(self, stage_name, content):
        with self.connection:
            self.cursor.execute("REPLACE INTO descs ('stage_name','content') VALUES (?,?)", (stage_name, content))
            self.connection.commit()

    def all_descs(self, stage_name):
        self.cursor.execute(f'SELECT * FROM descs WHERE stage_name LIKE "{stage_name}%"')
        data = self.cursor.fetchall()
        text = []
        for row in data:
            text.append(f"{row[0]}")
        print(text)
        return text[-1][-1]
    
    def all_pics(self, stage_name):
        self.cursor.execute(f'SELECT * FROM pics WHERE stage_name LIKE "{stage_name}%"')
        data = self.cursor.fetchall()
        text = []
        for row in data:
            text.append(f"{row[0]}")
        print(text)
        return text[-1][-1]

class UsersDatabase:
    def __init__(self):
        self.connection = sqlite3.connect(r'database\users.db')
        self.cursor = self.connection.cursor()
        self.connection.execute(
            '''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY,
                                                   name TEXT NOT NULL);'''
        )
    
    def add_user(self, user_id, nick):
        with self.connection:
            self.cursor.execute("REPLACE INTO users ('user_id','name') VALUES (?,?)", (user_id, nick))
            self.connection.commit()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,)).fetchall()
            print(bool(len(result)))
            return bool(len(result))
        
class InterDatabase:
    def __init__(self):
        self.connection = sqlite3.connect(r'database\users.db')
        self.cursor = self.connection.cursor()
        self.connection.execute(
            '''CREATE TABLE IF NOT EXISTS actions (stage_name TEXT PRIMARY KEY,
                                                   times INTEGER);'''
        )

    def add_visit(self, stage_name):
        with self.connection:
            self.cursor.execute("UPDATE actions SET times=times+1 WHERE stage_name=?", (stage_name,))
            self.connection.commit()
            
    def stats(self):
        self.cursor.execute(f'SELECT * FROM actions')
        data = self.cursor.fetchall()
        return data
        



