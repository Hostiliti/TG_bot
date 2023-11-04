import sqlite3 as sq
import json

class DataBase:
    def __init__(self):
        self.db = sq.connect('kwork_bot.db')
        self.cursor = self.db.cursor()
    #  Здесь я создаю базу данных для юзеров, где будут хрониться их id и id дня который у них сегодня. И бд для админа, где будут id дня, фраза, и таски на день  
    def db_connect(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY,
                        day_id INTEGER,
                        b_time,
                        l_time,
                        d_time);
        ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS days(
                        day_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phrase TEXT,
                        breakfast TEXT,
                        lunch TEXT,
                        dinner TEXT);
        ''')
        with open('Data\days.json', 'r', encoding='utf-8') as file1:
            data = json.load(file1)
            with open('Data\list.json', 'w', encoding='utf-8') as file2:
                days_ids = list(range(1, len(data)+1))
                j_list = {"list": days_ids}
                json.dump(j_list, file2)
            for d in data:
                self.cursor.execute(f'INSERT INTO days (phrase, breakfast, lunch, dinner) SELECT ?, ?, ?, ? WHERE NOT EXISTS(SELECT phrase, breakfast, lunch, dinner FROM days WHERE phrase = ? AND breakfast = ? AND lunch = ? AND dinner = ?)', (d.get('phrase'), d.get('breakfast'), d.get('lunch'), d.get('dinner'), d.get('phrase'), d.get('breakfast'), d.get('lunch'), d.get('dinner')))
                self.db.commit()
                
    # эта чехерня будет записывать пользователя в бд по комманде старт. И сразу будет ставить ему день 1. Повторное нажатие старт ничего не сломает, тк если он уже записан его номер дня не изменится.
    def db_add_user(self, user_id):
        self.cursor.execute(f'INSERT INTO users (user_id, day_id) VALUES (?, ?) ON CONFLICT DO NOTHING', (user_id, 1))
        self.db.commit()
        
    def db_add_user_time(self, user_id, times):
        self.cursor.execute(f'UPDATE users SET b_time = ?, l_time = ?, d_time = ? WHERE user_id LIKE ?', (times[0], times[1], times[2], user_id))
        self.db.commit()
        
    def db_get_day_id(self, user_id):
        self.cursor.execute('SELECT day_id FROM users WHERE user_id = ?', (user_id,))
        day_id = self.cursor.fetchone()[0]
        self.db.commit()
        return day_id
    
    #    это для юзера, будет чисто показывать таски на сегодня по day_id который хранится у пользователя в бд
    def db_show_today_tasks(self, day_id):
        self.cursor.execute('SELECT * FROM days WHERE day_id = ?', (day_id,))
        tasks = self.cursor.fetchone()
        tasks = f"Завтрак - {tasks[2]}.\nОбед - {tasks[3]}.\nУжин - {tasks[4]}."
        self.db.commit()
        return tasks
    
    # это для админа, тупо выведет ему все существующие дни
    def db_show_all_tasks(self):
        self.cursor.execute('SELECT * FROM days')
        all_tasks = self.cursor.fetchall()
        all_tasks = '\n'.join(' '.join(map(str, list(t))) for t in all_tasks)
        self.db.commit()
        return all_tasks
    
    def db_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        all_users = self.cursor.fetchall()
        self.db.commit()
        return all_users
    
    def db_get_task(self, day_id, time):
        self.cursor.execute(f'SELECT {time} FROM days WHERE day_id = ?', (day_id,))
        time = self.cursor.fetchone()[0]
        self.db.commit()
        return time
    
    def change_user_id(self, u_id, d_id):
        with open('Data\list.json', 'r', encoding='utf-8') as file:
            j_list = json.load(file).get('list')
            next_id = 1
            index = j_list.index(d_id)
            if index == len(j_list) - 1:
                pass
            else:
                next_id = j_list[index+1]
            self.cursor.execute(f'UPDATE users set day_id = ? WHERE user_id = ?', (next_id, u_id))
            self.db.commit()
