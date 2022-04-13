
import mysql.connector as database
from sql.db_connect import *
from windows.wind_mgmt import destroy_frame_content

def SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase):
    try:
        conn = database.connect(user = dbLogin, password = dbPassword, host = dbHost, database = dbDatabase)
    except database.Error as e:
        print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")
    return conn
conn = SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase)

def Get_SQL_Data(table, data1):
    sql_query = "SELECT " + data1 + " FROM " + table
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    prepare_table = get_sql.fetchall()
    table = []
    for item in prepare_table:
        table.append(item[0])
    return table

def Get_SQL_Data_ForUpdate(table, col_name, data):
    if table == "firma":
        table = "_firma"
    elif table == "stanowisko":
        table = "_stanowisko"
    elif table == "dzial":
        table = "_dzial"
    elif table == "lokalizacja":
        table = "_lokalizacja"
        col_name = "miasto"
    elif table == "umowa":
        table = "_umowa"
        col_name = "rodzaj"

    sql_query = "SELECT id FROM " + table + " WHERE " + col_name + " = '" + data + "'"
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    sql_id = get_sql.fetchall()[0][0]
    return sql_id

def Update_SQL_Data(table, col_name, value, where1, where2):
    sql_id = Get_SQL_Data_ForUpdate(col_name, col_name, value)

    sql_query = "UPDATE " + table + " SET " + col_name + " = " + str(sql_id) + " WHERE " + where1 + " = " + where2
    print(sql_query)
    update_sql = conn.cursor()
    update_sql.execute(sql_query)
    conn.commit()

def get_employees_by_department(department, frame):
        
    destroy_frame_content(frame)

    get_employees = conn.cursor()
    get_employees.execute("SELECT pracownicy.id, pracownicy.nazwisko, pracownicy.imie, _firma.firma, _stanowisko.stanowisko, _dzial.dzial, _lokalizacja.miasto, _umowa.rodzaj, pracownicy.karta FROM pracownicy LEFT JOIN _dzial ON pracownicy.dzial = _dzial.id LEFT JOIN _firma ON pracownicy.firma = _firma.id LEFT JOIN _umowa ON pracownicy.umowa = _umowa.id LEFT JOIN _stanowisko ON pracownicy.stanowisko = _stanowisko.id LEFT JOIN _lokalizacja ON pracownicy.lokalizacja = _lokalizacja.id WHERE _dzial.dzial = '%s' AND karta IS NOT NULL ORDER BY nazwisko" % department)
    employees = get_employees.fetchall()
    return employees

def get_employees_by_localization(localization, frame):
        
    destroy_frame_content(frame)

    get_employees = conn.cursor()
    get_employees.execute("SELECT pracownicy.id, pracownicy.nazwisko, pracownicy.imie, _firma.firma, _stanowisko.stanowisko, _dzial.dzial, _lokalizacja.miasto, _umowa.rodzaj, pracownicy.karta FROM pracownicy LEFT JOIN _dzial ON pracownicy.dzial = _dzial.id LEFT JOIN _firma ON pracownicy.firma = _firma.id LEFT JOIN _umowa ON pracownicy.umowa = _umowa.id LEFT JOIN _stanowisko ON pracownicy.stanowisko = _stanowisko.id LEFT JOIN _lokalizacja ON pracownicy.lokalizacja = _lokalizacja.id WHERE _lokalizacja.miasto = '%s' AND karta IS NOT NULL ORDER BY nazwisko" % localization)
    employees = get_employees.fetchall()
    return employees