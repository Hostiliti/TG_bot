import sqlite3 as sq
from datetime import datetime

class db:
    def __init__(self):
        self.db = sq.connect('tg_training_bot.db')
        self.cursor = self.db.cursor()
    #  Здесь я создаю базу данных для юзеров, где будут хрониться их id и id дня который у них сегодня. И бд для админа, где будут id дня, фраза, и таски на день  
    def db_connect(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY,
                        day_id INTEGER);
        ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks(
                        day_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phrase TEXT
                        breakfast TEXT,
                        lunch TEXT,
                        dinner TEXT);
        ''')
        
    #  это будет использоваться в комманде админа добавить таск, он тупо пишет фразу, таски, а id ставится автоматом  
    def db_add_task(self, phrase, breakfast, lunch, dinner):
        self.cursor.execute(f'INSERT INTO tasks (phrase, breakfast, lunch, dinner) VALUES (?, ?, ?, ?)', (phrase, breakfast, lunch, dinner))
        #self.cursor.execute(f'INSERT INTO trainings (user_id, training) SELECT ?, ? WHERE NOT EXISTS(SELECT * FROM trainings WHERE user_id = ? AND training = ?)', (u_id, training, u_id, training)) очень полезная строка кода, может пригодиться 
        self.db.commit()
        
    #   это для админа, по комманде удалить он может удалить день по id, который может посмотреть при помощи комманды show_all_tasks 
    def db_del_task(self, day_id):
        self.cursor.execute(f'DELETE FROM tasks WHERE task_id = ?', (day_id,))
        self.db.commit()
        
    # эта чехерня будет записывать пользователя в бд по комманде старт. И сразу будет ставить ему день 1. Повторное нажатие старт ничего не сломает, тк если он уже записан его номер дня не изменится.
    def db_add_user(self, user_id):
        self.cursor.execute(f'INSERT INTO users (user_id, task_id) VALUES (?, ?) ON CONFLICT DO NOTHING', (user_id, 1))
        self.db.commit()
        
    #    это для юзера, будет чисто показывать таски на сегодня по day_id который хранится у пользователя в бд
    def db_show_today_tasks(self, day_id):
        tself.cursor.execute('SELECT * FROM tasks WHERE day_id = ?', (day_id,))
        tasks = self.cursor.fetchone()
        tasks = f"Завтрак - {tasks[1]}.\nОбед - {tasks[2]}.\nУжин - {tasks[2]}."
        self.db.commit()
        return tasks
    
    # это для админа, тупо выведет ему все существующие дни
    def db_show_all_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        all_tasks = self.cursor.fetchall()
        all_tasks = '\n'.join(' '.join(map(str, list(t))) for t in all_tasks)
        self.db.commit()
        return all_tasks

