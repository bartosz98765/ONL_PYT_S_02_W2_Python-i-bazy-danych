new_database_query = """
CREATE DATABASE chat_test
"""

new_table_user_query = """
CREATE TABLE users(
id serial, 
username varchar(255) UNIQUE,
hashed_password varchar(80),
PRIMARY KEY(id)
)
"""

new_table_messages_query = """
CREATE TABLE messages(
id serial,
user_from_id serial,
user_to_id serial,
text text,
creation_date timestamp DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(id)
)
"""

sql_query_create_list = [new_database_query, new_table_user_query, new_table_messages_query]