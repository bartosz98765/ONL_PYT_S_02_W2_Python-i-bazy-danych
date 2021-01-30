import psycopg2


def connect():
    data = {
        'database': "chat_test",
        'user': "postgres",
        'password': "coderslab",
        'host': 'localhost',
        'port': 5432
    }
    conn = psycopg2.connect(**data)
    conn.autocommit = True
    return conn


if __name__ == '__main__':  # zabezpiecza przed wykonianiem wszystkiego co poniżej po wywyłaniu z innego pliku
    connection = connect()
    cursor = connection.cursor()

    query = """
            SELECT * FROM products;
            """

    cursor.execute(query)
    a = 5
    for i in range(a):
        txt = cursor.fetchone()
        print(txt)

    print(f"{cursor.fetchall()} - wskazuje od kolejnego miejsca na którym zakończył fetchone() {a}")

    print(cursor)
    connection.close()
