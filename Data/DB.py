import sqlite3 as sq

class DataBase:
    def __init__(self):
        self.db = sq.connect('kwork_bot.db')
        self.cursor = self.db.cursor()
    #  Здесь я создаю базу данных для юзеров, где будут хрониться их id и id дня который у них сегодня. И бд для админа, где будут id дня, фраза, и таски на день  
    def db_connect(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY,
                        day_id INTEGER);
        ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks(
                        day_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phrase TEXT,
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
        self.cursor.execute(f'INSERT INTO users (user_id, day_id) VALUES (?, ?) ON CONFLICT DO NOTHING', (user_id, 1))
        self.db.commit()
        
    def db_get_day_id(self, user_id):
        self.cursor.execute('SELECT day_id FROM users WHERE user_id = ?', (user_id,))
        day_id = self.cursor.fetchone()[0]
        self.db.commit()
        return day_id
    
    #    это для юзера, будет чисто показывать таски на сегодня по day_id который хранится у пользователя в бд
    def db_show_today_tasks(self, day_id):
        self.cursor.execute('SELECT * FROM tasks WHERE day_id = ?', (day_id,))
        tasks = self.cursor.fetchone()
        tasks = f"Завтрак - {tasks[2]}.\nОбед - {tasks[3]}.\nУжин - {tasks[4]}."
        self.db.commit()
        return tasks
    
    # это для админа, тупо выведет ему все существующие дни
    def db_show_all_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        all_tasks = self.cursor.fetchall()
        all_tasks = '\n'.join(' '.join(map(str, list(t))) for t in all_tasks)
        self.db.commit()
        return all_tasks
    
    def db_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        all_users = self.cursor.fetchall()
        all_users = [list(u) for u in all_users]
        self.db.commit()
        return all_users
    
    def db_get_breakfast(self, day_id):
        self.cursor.execute('SELECT breakfast FROM tasks WHERE day_id = ?', (day_id,))
        breakfast = self.cursor.fetchone()[0]
        self.db.commit()
        return breakfast
        
    def db_get_lunch(self, day_id):
        self.cursor.execute('SELECT lunch FROM tasks WHERE day_id = ?', (day_id,))
        lunch = self.cursor.fetchone()[0]
        self.db.commit()
        return lunch
    
    def db_get_dinner(self, day_id):
        self.cursor.execute('SELECT dinner FROM tasks WHERE day_id = ?', (day_id,))
        dinner = self.cursor.fetchone()[0]
        self.db.commit()
        return dinner

db = DataBase()
db.db_connect()

