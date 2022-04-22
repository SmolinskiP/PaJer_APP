from tkinter import *
import hashlib
from sql.db_connect import *
import mysql.connector as database

def validate_login(uname, input_password):
    db_password = ""
    try:
        from sql.db_data_functions import SQL_Connect
        conn = SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort)
    except database.Error as e:
        print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")

    try:
        get_db_password = conn.cursor()
        get_db_password.execute("SELECT haslo FROM konta WHERE login='%s'" % uname)
        db_password = get_db_password.fetchall()[0][0]
    except Exception as e:
        print("Error 77")
        print(e)
    if hashlib.sha256(input_password.encode()).hexdigest() == db_password:
        return True
    else:
        return False

def change_password_sql():
    actual_pwd = actual_password.get()
    pwd = password.get()
    pwd2 = password2.get()
    print(actual_pwd)
    print(pwd)
    print(pwd2)

    if pwd != pwd2:
        message.set("Hasla roznia sie od siebie. Sprobuj jeszcze raz")
    elif actual_pwd == "" or pwd == "" or pwd2 == "":
        message.set("Uzupelnij prosze wszystkie pola")
    else:
        from login_form.login_form import uname
        if validate_login(uname, actual_pwd) == True:
            pwd = hashlib.sha256(pwd.encode()).hexdigest()
            from sql.db_data_functions import SQL_Connect
            conn = SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort)
            update_db_password = conn.cursor()
            sql_query = "UPDATE konta SET haslo = '" + pwd + "' WHERE login = '" + uname + "'"
            print(sql_query)
            update_db_password.execute(sql_query)
            conn.commit()
            message.set("Gitara!!!")
            newWindow.destroy()
        else:
            message.set("Wrong password!!!")


def Change_Password():
    global newWindow
    newWindow = Toplevel()
    newWindow.title("Zmiana hasla")
    newWindow.geometry("300x250")
    
    global message
    global actual_password
    global password
    global password2
    message = StringVar()
    actual_password = StringVar()
    password = StringVar()
    password2 = StringVar()

    Label(newWindow, width="300", text="Wprowadz dane ponizej", bg="orange",fg="white").pack()
    Label(newWindow, text="Aktualne haslo * ").place(x=5,y=40)
    Entry(newWindow, textvariable=actual_password).place(x=90,y=42)
    Label(newWindow, text="Nowe haslo * ").place(x=5,y=80)
    Entry(newWindow, textvariable=password ,show="*").place(x=90,y=82)
    Label(newWindow, text="Powtorz\nNowe haslo * ").place(x=5,y=120)
    Entry(newWindow, textvariable=password2 ,show="*").place(x=90,y=129)
    Label(newWindow, text="",textvariable=message).place(x=60,y=200)
    Button(newWindow, text="Zmien haslo", width=10, height=1, bg="orange", command=change_password_sql).place(x=105,y=160)