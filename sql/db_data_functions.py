
import mysql.connector as database
from sql.db_connect import *


def SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort):
    try:
        conn = database.connect(user = dbLogin, password = dbPassword, host = dbHost, database = dbDatabase, port = dbPort)
    except database.Error as e:
        print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")
    return conn
conn = SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort)

def Get_Single_SQL_Data(table, data, where):
    sql_query = "SELECT " + data + " FROM " + table + " WHERE id = " + where
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    output = get_sql.fetchall()[0][0]
    return output

def Get_SQL_Data(table, data1):
    sql_query = "SELECT " + data1 + " FROM " + table
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    prepare_table = get_sql.fetchall()
    table = []
    for item in prepare_table:
        table.append(item[0])
    return table

def Get_SQL_Employees_ID():
    sql_query = "SELECT nazwisko, imie, id FROM pracownicy ORDER BY nazwisko"
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    prepare_dict = get_sql.fetchall()
    emp_dict = {}
    for item in prepare_dict:
        employee_name = item[0] + " " + item[1]
        emp_dict[employee_name] = item[2]
    return emp_dict

def Get_SQL_Data_2(table, data1, data2):
    sql_query = "SELECT " + data1 + ", " + data2 + " FROM " + table
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

def Update_SQL_Data_Prepared(prepared_query):
    print(prepared_query)
    update_sql = conn.cursor()
    update_sql.execute(prepared_query)
    conn.commit()
    

def Remove_SQL_Data(table, where1, where2):
    sql_query = "DELETE FROM " + table + " WHERE " + where1 + " = " + where2
    update_sql = conn.cursor()
    update_sql.execute(sql_query)
    print(sql_query)
    conn.commit()

def get_employees_by_department(department, frame):
    from windows.wind_mgmt import destroy_frame_content
    destroy_frame_content(frame)

    get_employees = conn.cursor()
    get_employees.execute("SELECT pracownicy.id, pracownicy.nazwisko, pracownicy.imie, _firma.firma, _stanowisko.stanowisko, _dzial.dzial, _lokalizacja.miasto, _umowa.rodzaj, pracownicy.karta FROM pracownicy LEFT JOIN _dzial ON pracownicy.dzial = _dzial.id LEFT JOIN _firma ON pracownicy.firma = _firma.id LEFT JOIN _umowa ON pracownicy.umowa = _umowa.id LEFT JOIN _stanowisko ON pracownicy.stanowisko = _stanowisko.id LEFT JOIN _lokalizacja ON pracownicy.lokalizacja = _lokalizacja.id WHERE _dzial.dzial = '%s' AND karta IS NOT NULL ORDER BY nazwisko" % department)
    employees = get_employees.fetchall()
    return employees

def get_employees_by_localization(localization, frame):
    from windows.wind_mgmt import destroy_frame_content
    destroy_frame_content(frame)

    get_employees = conn.cursor()
    get_employees.execute("SELECT pracownicy.id, pracownicy.nazwisko, pracownicy.imie, _firma.firma, _stanowisko.stanowisko, _dzial.dzial, _lokalizacja.miasto, _umowa.rodzaj, pracownicy.karta FROM pracownicy LEFT JOIN _dzial ON pracownicy.dzial = _dzial.id LEFT JOIN _firma ON pracownicy.firma = _firma.id LEFT JOIN _umowa ON pracownicy.umowa = _umowa.id LEFT JOIN _stanowisko ON pracownicy.stanowisko = _stanowisko.id LEFT JOIN _lokalizacja ON pracownicy.lokalizacja = _lokalizacja.id WHERE _lokalizacja.miasto = '%s' AND karta IS NOT NULL ORDER BY nazwisko" % localization)
    employees = get_employees.fetchall()
    return employees

def get_occurence_by_employee(employee_id, frame):
    from windows.wind_mgmt import destroy_frame_content
    destroy_frame_content(frame)

    get_occurance = conn.cursor()
    get_occurance.execute("SELECT pracownicy.id, pracownicy.nazwisko, pracownicy.imie, obecnosc.time, _action.action, obecnosc.komentarz, obecnosc.id FROM obecnosc LEFT JOIN pracownicy ON pracownicy.id = obecnosc.pracownik LEFT JOIN _action ON obecnosc.action = _action.id WHERE obecnosc.pracownik = '%s' ORDER BY nazwisko" % str(employee_id))
    occurance = get_occurance.fetchall()
    return occurance

def get_occurence_by_entry_time(entry_time, frame):
    from windows.wind_mgmt import destroy_frame_content
    destroy_frame_content(frame)

    get_occurance = conn.cursor()
    get_occurance.execute("SELECT pracownicy.id, pracownicy.nazwisko, pracownicy.imie, obecnosc.time, _action.action, obecnosc.komentarz, obecnosc.id FROM obecnosc LEFT JOIN pracownicy ON pracownicy.id = obecnosc.pracownik LEFT JOIN _action ON obecnosc.action = _action.id WHERE obecnosc.time LIKE '" + str(entry_time) + "%' ORDER BY nazwisko")
    occurance = get_occurance.fetchall()
    return occurance

def get_occurence_by_entry_time_two(entry_time_from, entry_time_to, entry_employee, frame):
    entry_time_from = str(entry_time_from) + " 00:00:01"
    entry_time_to = str(entry_time_to) + " 23:59:59"
    if entry_employee == "*":
        sql_query = "SELECT pracownicy.id, pracownicy.nazwisko, pracownicy.imie, obecnosc.time, _action.action, obecnosc.komentarz, obecnosc.id FROM obecnosc LEFT JOIN pracownicy ON pracownicy.id = obecnosc.pracownik LEFT JOIN _action ON obecnosc.action = _action.id WHERE obecnosc.time >= '" + entry_time_from + "' AND obecnosc.time <= '" + entry_time_to + "' ORDER BY nazwisko, imie, time"
    else:
        sql_query = "SELECT pracownicy.id, pracownicy.nazwisko, pracownicy.imie, obecnosc.time, _action.action, obecnosc.komentarz, obecnosc.id FROM obecnosc LEFT JOIN pracownicy ON pracownicy.id = obecnosc.pracownik LEFT JOIN _action ON obecnosc.action = _action.id WHERE obecnosc.time >= '" + entry_time_from + "' AND obecnosc.time <= '" + entry_time_to + "' AND pracownik = " + str(entry_employee) + " ORDER BY nazwisko, imie, time"
    from windows.wind_mgmt import destroy_frame_content
    destroy_frame_content(frame)
    
    get_occurance = conn.cursor()
    get_occurance.execute(sql_query)
    occurance = get_occurance.fetchall()
    return occurance