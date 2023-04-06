import sqlite3


class DBController:

    def _connect_decorator(function):

        def wrapper(*args, **kwargs):
            conn = sqlite3.connect(args[0].db_name)
            conn.execute("PRAGMA foreign_keys = 1")
            conn.commit()
            cursor = conn.cursor()
            result = function(cursor, *args, **kwargs)
            conn.commit()
            conn.close()
            return result

        return wrapper

    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.create_database()

    @_connect_decorator
    def create_database(c, self):
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                credits INTEGER
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                name TEXT,
                price INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

    @_connect_decorator
    def create_user(c, self, username, credits=0):
        c.execute('INSERT INTO users (username, credits) VALUES (?, ?)',
                  (username, credits))

    @_connect_decorator
    def get_user(c, self, username):

        c.execute('SELECT * FROM users WHERE username = ?', (username, ))
        user = c.fetchone()

        if user is None:
            return None

        return {'id': user[0], 'username': user[1], 'credits': user[2]}

    @_connect_decorator
    def create_item(c, self, user_id, name, price):

        c.execute('INSERT INTO items (user_id, name, price) VALUES (?, ?, ?)',
                  (user_id, name, price))

    @_connect_decorator
    def get_items(c, self, user_id):

        c.execute('SELECT * FROM items WHERE user_id = ?', (user_id, ))
        items = c.fetchall()

        return [{
            'id': item[0],
            'user_id': item[1],
            'name': item[2],
            'price': item[3]
        } for item in items]

    @_connect_decorator
    def get_item_with_name(c, self, user_id, item_name):

        c.execute('SELECT * FROM items WHERE user_id = ? AND name = ?',
                  (user_id, item_name))
        items = c.fetchall()

        return [{
            'id': item[0],
            'user_id': item[1],
            'name': item[2],
            'price': item[3]
        } for item in items]

    @_connect_decorator
    def update_item(c, self, item_id, name, price):

        c.execute('UPDATE items SET name = ?, price = ? WHERE id = ?',
                  (name, price, item_id))

    @_connect_decorator
    def delete_item(c, self, item_id):

        c.execute('DELETE FROM items WHERE id = ?', (item_id, ))

        if c.rowcount == 0:
            raise sqlite3.IntegrityError('Item does not exist')

    @_connect_decorator
    def add_credits(c, self, user_id, credits):

        c.execute('UPDATE users SET credits = credits + ? WHERE id = ?',
                  (credits, user_id))

    @_connect_decorator
    def subtract_credits(c, self, user_id, credits):

        c.execute('SELECT credits FROM users WHERE id = ?', (user_id, ))
        user = c.fetchone()
        if user is None:
            raise sqlite3.IntegrityError('User does not exist')

        current_credits = user[0]
        if current_credits < credits:
            raise ValueError('User does not have enough credits')

        c.execute('UPDATE users SET credits = credits - ? WHERE id = ?',
                  (credits, user_id))
