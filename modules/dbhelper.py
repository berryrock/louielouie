import sqlite3

class DBhelper():
    def __init__(self, dbname="louie.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS users (user_id, name, weight, lenght, birthday, dish, recomendations, step, acc, call, prev_call, prev_prev_call)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_user(self, user_id, acc):
        stmt = 'INSERT INTO users (user_id, acc) VALUES (?, ?)'
        args = (user_id, acc,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def set_step(self, user_id, step):
        stmt = 'UPDATE users SET step = "{}" WHERE user_id = {}'.format(step, user_id)
        self.conn.execute(stmt)
        self.conn.commit()

    def get_step(self, user_id):
        stmt = 'SELECT step FROM users WHERE user_id = "{}"'.format(user_id)
        return [x[0] for x in self.conn.execute(stmt)]

    def set_data(self, user_id, type_of_data, value):
        stmt = 'UPDATE users SET {} = "{}" WHERE user_id = "{}"'.format(type_of_data, value, user_id)
        self.conn.execute(stmt)
        self.conn.commit()

    def get_data(self, user_id, type_of_data):
        stmt = 'SELECT {} FROM users WHERE user_id = "{}"'.format(type_of_data, user_id)
        return [x[0] for x in self.conn.execute(stmt)]

    def print_user_data(self, user_id):
        stmt = 'SELECT * FROM users WHERE user_id = "{}"'.format(user_id)
        return [x[0] for x in self.conn.execute(stmt)]

    def get_call(self, user_id):
        stmt = 'SELECT call, prev_call, prev_prev_call FROM users WHERE user_id = "{}"'.format(user_id)
        calls = [x for x in self.conn.execute(stmt)]
        calls = list(calls[0])
        return calls

    def set_call(self, user_id, value):
        previous_calls = self.get_call(user_id)
        if len(previous_calls) < 1:
            previous_calls = ['Empty', 'Empty']
        elif len(previous_calls) < 2:
            previous_calls.append('Empty')
        stmt = 'UPDATE users SET call = "{}", prev_call = "{}", prev_prev_call = "{}" WHERE user_id = "{}"'.format(value, previous_calls[0], previous_calls[1], user_id)
        self.conn.execute(stmt)
        self.conn.commit()

    def clear_call(self, user_id):
        stmt = 'UPDATE users SET call = "", prev_call = "", prev_prev_call = "" WHERE user_id = "{}"'.format(user_id)
        self.conn.execute(stmt)
        self.conn.commit()
