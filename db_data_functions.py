
import mysql.connector as database
from db_connect import *
import numpy as np

try:
    conn = database.connect(user = dbLogin, password = dbPassword, host = dbHost, database = dbDatabase)
except database.Error as e:
    print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")


