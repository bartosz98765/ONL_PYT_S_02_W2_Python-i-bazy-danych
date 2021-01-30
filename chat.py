import argparse
import models
from dbconnection import connect

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--to", help="recipient")
parser.add_argument("-s", "--send", help="message")
parser.add_argument("-l", "--list", help="list messages", action="store_true")

args = parser.parse_args()

if args.list:
    print('list of messages:')
    conn = connect()
    cursor1 = conn.cursor()
    load_user = models.User.load_user_by_username(cursor1, args.username)
    all_user_messages = models.Message.load_all_messages(cursor1, load_user.id)
    conn.close()
    for row in all_user_messages:
        print(f"Wiadomość {row[0]}: Czas wysłania: {row[4]}\n Treść wiadomości: {row[3]}\n")

if args.send:
    conn = connect()
    cursor1 = conn.cursor()
    load_user_from = models.User.load_user_by_username(cursor1, args.username)
    load_user_to = models.User.load_user_by_username(cursor1, args.to)
    message1 = models.Message(load_user_from.id, load_user_to.id, args.send)
    message1.save_message_to_db(cursor1)
    conn.close()
    print(message1._id, message1.creation_data)