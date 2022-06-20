import sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscribers(self, status=True):
        """ Get all activ subscribers """
        with self.connection:
            return self.cursor.execute('SELECT * FROM `subscribers` WHERE `status` = ?', (status,)).fetchall()

    def get_not_subscribers(self):
        """ Get not activ subscribers """
        with self.connection:
            return self.cursor.execute('SELECT `status` FROM `subscribers`')

    def subscriber_exists(self, user_id):
        """ Check user in DB """
        with self.connection:
            result = self.cursor.execute(
                'SELECT * FROM `subscribers` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        """ Add new subscriber """
        with self.connection:
            return self.cursor.execute('INSERT INTO `subscribers` (`user_id`, `status`) VALUES(?, ?)', (user_id, status))

    def update_subscribtion(self, user_id, status):
        """ Update user status """
        with self.connection:
            return self.cursor.execute("UPDATE `subscribers` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def delete_subscribtion(self, user_id):
        """ Del user """
        with self.connection:
            return self.cursor.execute(f'DELETE FROM subscribers WHERE user_id= {user_id}')

    def close(self):
        self.connection.close()
