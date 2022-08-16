import sqlite3 as sql
import bcrypt
import getpass

db='user.db'

connection= sql.connect(db)

cursor=connection.cursor()


cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_details (
        username CHAR(60) NOT NULL DEFAULT '',
        password CHAR(60) NOT NULL DEFAULT ''
        )""")

connection.commit()
connection.close()



def accept_credentials():
    username=input("enter username: ")
    plaintext_password=getpass.getpass(prompt="enter password: ")
    password=bcrypt.hashpw(plaintext_password , bcrypt.gensalt())
    return username,password


def commit_to_db(username,password):
    connection=sql.connect(db)
    cursor=connection.cursor()
    cursor.execute("""INSERT INTO user_details values (?,?)""", (username,password))
    connection.commit()
    connection.close()


def show_all_db_contents():
    connection=sql.connect(db)
    cursor=connection.cursor()
    cursor.execute("""SELECT * FROM user_details""")
    all_data=cursor.fetchall()
    connection.commit()
    connection.close()
    return all_data


def show_db_content_username(username):
    connection=sql.connect(db)
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM user_details where username= ?" , (username,))
    all_data=cursor.fetchall()
    connection.commit()
    connection.close()
    return all_data


username1,password1=accept_credentials()
commit_to_db(username1,password1)

username2,password2=accept_credentials()
commit_to_db(username2,password2)

print(show_all_db_contents())

whichuser=input("Enter username to fetch the details: ")
whichpass=getpass.getpass(prompt="enter corresponding password: ")
fetched_user_tuple=show_db_content_username(whichuser)
print(fetched_user_tuple)

if bcrypt.checkpw(whichpass,fetched_user_tuple[0][1]):
    print(f"Welecome {whichuser}")
else:
    print("Invalid username")



