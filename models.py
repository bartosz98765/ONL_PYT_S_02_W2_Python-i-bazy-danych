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
        else:
            sql_query = f"""
                        UPDATE users SET username = '{self.username}', hashed_password = '{self.hashed_password}' 
                        WHERE id = {self.id};
                        """
            cursor.execute(sql_query)
            return True

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
                    SELECT * FROM users;
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


class Message:

    def __init__(self, from_id, to_id, text):
        self._id = None
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_data = None

    @property
    def id(self):
        return self._id

    def save_message_to_db(self, cursor):
        if self._id is None:
            sql_query = f"""
                        INSERT INTO messages (user_from_id, user_to_id, text) 
                        VALUES ({self.from_id}, {self.to_id}, '{self.text}') RETURNING id, creation_date
                        """
            cursor.execute(sql_query)
            data = cursor.fetchone()
            self._id = data[0]
            self.creation_data = data[1]
            return True
        else:
            sql_query = f"""
                        UPDATE messages SET user_from_id={self.from_id}, user_to_id={self.to_id}, text='{self.text}'
                        WHERE id={self._id}
                        """
            cursor.execute(sql_query)
            return True

    @staticmethod
    def load_all_messages(cursor):
        all_loaded_messages = []
        sql_query = """
                    SELECT * FROM messages;
                    """
        cursor.execute(sql_query)
        data = cursor.fetchall()
        if data:
            for row in data:
                # mid, fromid, toid, txt, creatdata = data
                # loaded_message = Message(fromid, toid, txt)
                # loaded_message._id = mid
                # loaded_message.creation_data = creatdata
                all_loaded_messages.append(row)
            return all_loaded_messages
        return None

    @staticmethod
    def start():
        conn = connect()
        cursor1 = conn.cursor()
        all_msg_list = Message.load_all_messages(cursor1)
        conn.close()
        for row in all_msg_list:
            print(row)


if __name__ == '__main__':
    pass

#NEW USER
    # user1 = User(username='Janina', password='moje_haslo')
    # conn = connect()
    # cursor1 = conn.cursor()
    # user1.save_to_db(cursor1)
    # load_user = User.load_user_by_id(cursor1, 22)
    # conn.close()
    #




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
    # print(all_user_list)

# TEST: SAVE NEW PASSWORD
#     conn = connect()
#     cursor1 = conn.cursor()
#     loaded_user = User.load_user_by_username(cursor1, 'Olga')
#     print('Przed zmianą:')
#     print(loaded_user.id, loaded_user.username, loaded_user.hashed_password)
#     conn.close()
#
#     conn = connect()
#     cursor2 = conn.cursor()
#     # loaded_user.username = "Olga"
#     loaded_user.hashed_password = "mojehaslo321"
#     loaded_user.save_to_db(cursor2)
#     print('Po zmianie:')
#     print(loaded_user.id, loaded_user.username, loaded_user.hashed_password)
#     conn.close()
#-------------------------------------

    # conn = connect()
    # cursor1 = conn.cursor()
    # loaded_user = User.load_user_by_id(cursor1, 3)
    # print('Przed zmianą:')
    # print(loaded_user)
    # conn.close()
    #
    # if loaded_user is not None:
    #     conn = connect()
    #     cursor2 = conn.cursor()
    #     loaded_user.delete_user(cursor2)
    #     conn.close()
    # else:
    #     print("Użytkownik nie istnieje")
    # message1 = Message(from_id=11, to_id=22, text='Moja nowa wiadomość')
    # conn = connect()
    # cursor1 = conn.cursor()
    # message1.save_message_to_db(cursor1)
    # conn.close()
    # print(message1._id, message1.creation_data)


    # Message.start()