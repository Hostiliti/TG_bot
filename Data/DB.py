import sqlite3 as sq
from datetime import datetime

class db:
    def __init__(self):
        self.db = sq.connect('tg_training_bot.db')
        self.cursor = db.cursor()
        
    def db_connect(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY);
        ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS trainings(
                        user_id INTEGER,
                        training TEXT);
        ''')
        
    def db_write_training(self, u_id, training):
        self.cursor.execute(f'INSERT INTO trainings (user_id, training) SELECT ?, ? WHERE NOT EXISTS(SELECT * FROM trainings WHERE user_id = ? AND training = ?)', (u_id, training, u_id, training))
        self.db.commit()
        
    def db_del_training(self, u_id, training):
        self.cursor.execute(f'DELETE FROM trainings WHERE user_id = ? AND training = ?', (u_id, training))
        self.db.commit()

    def db_write_user(self, u_id):
        self.cursor.execute(f'INSERT INTO users VALUES (?) ON CONFLICT DO NOTHING', (u_id,))
        self.db.commit()
        
    def db_show_all(self, u_id):
        self.cursor.execute('SELECT training FROM trainings WHERE user_id = ?', (u_id,))
        trainings = self.cursor.fetchall()
        self.db.commit()
        return trainings

    def db_get_all_id(self):
        self.cursor.execute('SELECT * FROM users')
        all_id = self.cursor.fetchall()
        self.db.commit()
        return all_id

    def db_del_old(self, trainings, u_id):
        for t in trainings:
            self.cursor.execute('DELETE FROM trainings WHERE training = ? AND user_id = ?', (t, u_id))
            self.db.commit()
