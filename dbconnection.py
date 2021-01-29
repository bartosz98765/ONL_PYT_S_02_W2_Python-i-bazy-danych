import psycopg2

def connect():
    data = {
        'database' : "chat",
        'user' : "postgres",
        'password' : "coderslab",
        'host' : 'localhost',
        'port' : 5432
    }
    conn = psycopg2.connect(**data)
    conn.autocommit = True
    return conn

if __name__ == '__main__':
    connection = connect()
    cursor = connection.cursor()
    print(cursor)
    connection.close()
