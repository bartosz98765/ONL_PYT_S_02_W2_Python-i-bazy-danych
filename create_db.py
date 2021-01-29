from dbconnection import connect
from sql_query_create import sql_query_create_list


def create_db(query_list=None):
    if query_list == None:
        query_list = sql_query_create_list
        conn = connect()
        cursor = conn.cursor()
        for query in query_list:
            try:
                cursor.execute(query)
            except Exception as errorvalue:
                print(f"Error: {errorvalue}, {type(errorvalue)}")
                txt = query.split('\n')[1][:-1]
                print(f"In query: {txt}")


if __name__ == '__main__':
    create_db()
