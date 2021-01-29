from clcrypto import hash_password
from dbconnection import connect


class User:

    def __init__(self, username="", password="", salt=""):
        self._id = None
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=''):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id is None:
            sql_query = f"""
                        INSERT INTO users(username, hashed_password) 
                        VALUES ('{self.username}','{self.hashed_password}') 
                        RETURNING id;
                        """
            cursor.execute(sql_query)
            self._id = cursor.fetchone()[0]
            return True
        if self._id is not None:
            sql_query = f"""
                        UPDATE users SET username = '{self.username}', hashed_password = '{self.hashed_password}' 
                        WHERE id = {self.id};
                        """
            cursor.execute(sql_query)
            return True
        return False

    @staticmethod
    def load_user_by_username(cursor, username):
        sql_query = f"""
                    SELECT id, username, hashed_password FROM users WHERE username = '{username}'
                    """
        cursor.execute(sql_query)
        data = cursor.fetchone()
        if data:  # if data exists then True
            userid, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = userid
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_id(cursor, userid):
        sql_query = f"""
                    SELECT id, username, hashed_password FROM users WHERE id = '{userid}'
                    """
        cursor.execute(sql_query)
        data = cursor.fetchone()
        if data:  # if data exists then True
            userid, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = userid
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        all_user_list = []
        sql_query = f"""
                    SELECT id, username, hashed_password FROM users;
                    """
        cursor.execute(sql_query)
        data = cursor.fetchall()
        if data:  # if data exists then True
            for element in data:
                userid, username, hashed_password = element
                loaded_user = User(username)
                loaded_user._id = userid
                loaded_user._hashed_password = hashed_password
                all_user_list.append(loaded_user)
            return all_user_list
        else:
            return None

    def delete_user(self, cursor):
        if self._id is not None:
            sql_query = f"""
                        DELETE FROM users WHERE id={self._id}
                        """
            cursor.execute(sql_query)
            self._id = None
            return True
        return False









if __name__ == '__main__':
    # user1 = User(username='Janina', password='moje_haslo')

    # conn = connect()
    # cursor1 = conn.cursor()
    # user1.save_to_db(cursor1)
    # load_user = User.load_user_by_id(cursor1, 22)
    # conn.close()

    # conn = connect()
    # cursor1 = conn.cursor()
    # load_user = User.load_user_by_id(cursor1, 22)
    # conn.close()
    # if load_user is not None:
    #     print(load_user.id, load_user.username, load_user.hashed_password)
    # else:
    #     print(load_user)

    # conn = connect()
    # cursor1 = conn.cursor()
    # all_user_list = User.load_all_users(cursor1)
    # conn.close()
    # for row in all_user_list:
    #     print(row._id, row.username)

    # conn = connect()
    # cursor1 = conn.cursor()
    # loaded_user = User.load_user_by_id(cursor1, 1)
    # print('Przed zmianą:')
    # print(loaded_user.id, loaded_user.username, loaded_user.hashed_password)
    # conn.close()
    #
    # conn = connect()
    # cursor2 = conn.cursor()
    # loaded_user.username = "Olga"
    # loaded_user.hashed_password = "dfsdfsdfs"
    # loaded_user.save_to_db(cursor2)
    # print('Po zmianie:')
    # print(loaded_user.id, loaded_user.username, loaded_user.hashed_password)
    # conn.close()

    conn = connect()
    cursor1 = conn.cursor()
    loaded_user = User.load_user_by_id(cursor1, 3)
    print('Przed zmianą:')
    print(loaded_user)
    conn.close()

    if loaded_user is not None:
        conn = connect()
        cursor2 = conn.cursor()
        loaded_user.delete_user(cursor2)
        conn.close()
    else:
        print("Użytkownik nie istnieje")