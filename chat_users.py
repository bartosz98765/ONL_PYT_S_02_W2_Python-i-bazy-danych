import argparse
import models
from dbconnection import connect

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-n", "--new_pass", help="new password")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user password", action="store_true")
parser.add_argument("-l", "--list", help="list messages", action="store_true")


# try:
args = parser.parse_args()
if args.list:
    print('Users list:')
    conn = connect()
    cursor1 = conn.cursor()
    all_user_list = models.User.load_all_users(cursor1)
    conn.close()
    for row in all_user_list:
        print(row.username)
elif args.username and args.password:
    if args.delete:
        print(f'Delete user: {args.username}')
        conn = connect()
        cursor1 = conn.cursor()
        loaded_user = models.User.load_user_by_username(cursor1, args.username)
        conn.close()
        if loaded_user is not None:
            conn = connect()
            cursor2 = conn.cursor()
            loaded_user.delete_user(cursor2)
            conn.close()
        else:
            print(f"Użytkownik {args.username} nie istnieje")
    elif args.edit and args.new_pass:
        print('Edit password')
        conn = connect()
        cursor1 = conn.cursor()
        loaded_user = models.User.load_user_by_username(cursor1, args.username)
        conn.close()
        if loaded_user is not None:
            conn = connect()
            cursor2 = conn.cursor()
            loaded_user.hashed_password = args.new_pass
            loaded_user.save_to_db(cursor2)
            conn.close()
        else:
            print(f"Użytkownik {args.username} nie istnieje")
    else:
        print('New user')
        user1 = models.User(args.username, args.password)
        conn = connect()
        cursor1 = conn.cursor()
        user1.save_to_db(cursor1)
        conn.close()
else:
    print('Błędne argumenty')
# except:
#     print('Błędne argumenty')
#     # parser.print_help()

# if args.list:
#     models.Message.start()
#
# if args.username:
#     print(f"imię: {args.username}")


# print(args.list)

# parser.print_help()

# print(parser.parse_args('-u Bartek'.split()))
