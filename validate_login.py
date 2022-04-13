import mysql.connector as database
import hashlib
from db_connect import *

def validate_login(uname, input_password):
    db_password = ""
    try:
        conn = database.connect(user = dbLogin, password = dbPassword, host = dbHost, database = dbDatabase)
    except database.Error as e:
        print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")

    try:
        get_db_password = conn.cursor()
        get_db_password.execute("SELECT password FROM employees WHERE login='%s'" % uname)
        db_password = get_db_password.fetchall()[0][0]
    except:
        print("Error 77")
    if hashlib.sha256(input_password.encode()).hexdigest() == db_password:
        return True
    else:
        return False

