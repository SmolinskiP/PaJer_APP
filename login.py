
from login_form import *
from tkinter import *
import tkinter as tk
from tkinter import *
import mysql.connector as database
from db_connect import *

login_form()



try:
    conn = database.connect(user = dbLogin, password = dbPassword, host = dbHost, database = dbDatabase)
except database.Error as e:
    print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")

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

umowy = Get_SQL_Data("_umowa", "rodzaj")
departments = Get_SQL_Data("_dzial", "dzial")
stanowiska = Get_SQL_Data("_stanowisko", "stanowisko")
firmy = Get_SQL_Data("_firma", "firma")
miasta = Get_SQL_Data("_lokalizacja", "miasto")

global employeesframe
global employeescanvas

topframe = Frame(main_window)
topframe.grid(row=0, column=1, sticky='w')

leftsquare = Frame(main_window)
leftsquare.grid(row=0, column=0)

leftframe = Frame(main_window)
leftframe.grid(row=1, column=0, sticky='n')

employeescanvas = Frame(main_window, width=500, height=400)
employeescanvas.grid(row=1, column=1)

employeesframe = Canvas(employeescanvas, bg='#4A7A8C', width=150, height=150, scrollregion=(0,0,2000,2000))
employeesframe.configure(scrollregion=employeesframe.bbox("all"))
vertibar=Scrollbar(
    employeescanvas,
    orient=VERTICAL
    )
vertibar.pack(side=RIGHT,fill=Y)
vertibar.config(command=employeesframe.yview)
employeesframe.config(width=1300,height=600)
employeesframe.config(
    yscrollcommand=vertibar.set
    )
employeesframe.pack(expand=True,side=LEFT)

department = StringVar(main_window)
department.set("Dzial")
localization = StringVar(main_window)
localization.set("Miasto")


def destroy_frame_content(frame):
    for content in employeesframe.winfo_children():
        content.destroy()

def get_employees_by_department(department):
        
    destroy_frame_content(employeesframe)

    get_employees = conn.cursor()
    get_employees.execute("SELECT pracownicy.id, pracownicy.nazwisko, pracownicy.imie, _firma.firma, _stanowisko.stanowisko, _dzial.dzial, _lokalizacja.miasto, _umowa.rodzaj, pracownicy.karta FROM pracownicy LEFT JOIN _dzial ON pracownicy.dzial = _dzial.id LEFT JOIN _firma ON pracownicy.firma = _firma.id LEFT JOIN _umowa ON pracownicy.umowa = _umowa.id LEFT JOIN _stanowisko ON pracownicy.stanowisko = _stanowisko.id LEFT JOIN _lokalizacja ON pracownicy.lokalizacja = _lokalizacja.id WHERE _dzial.dzial = '%s' AND karta IS NOT NULL ORDER BY nazwisko" % department)
    employees = get_employees.fetchall()
    return employees

def get_employees_by_localization(localization):
        
    destroy_frame_content(employeesframe)

    get_employees = conn.cursor()
    get_employees.execute("SELECT pracownicy.id, pracownicy.nazwisko, pracownicy.imie, _firma.firma, _stanowisko.stanowisko, _dzial.dzial, _lokalizacja.miasto, _umowa.rodzaj, pracownicy.karta FROM pracownicy LEFT JOIN _dzial ON pracownicy.dzial = _dzial.id LEFT JOIN _firma ON pracownicy.firma = _firma.id LEFT JOIN _umowa ON pracownicy.umowa = _umowa.id LEFT JOIN _stanowisko ON pracownicy.stanowisko = _stanowisko.id LEFT JOIN _lokalizacja ON pracownicy.lokalizacja = _lokalizacja.id WHERE _lokalizacja.miasto = '%s' AND karta IS NOT NULL ORDER BY nazwisko" % localization)
    employees = get_employees.fetchall()
    print(localization)
    print(employees)
    return employees



def Create_Top_table():
    key = "topframe"
    dict_firma[key] = Frame(employeesframe)
    canvas_toplabel = employeesframe.create_window(650, 20, window=dict_firma[key])
    #dict_firma[key].grid(row=0, column=0)
    x = 0
    entries = ["LP", "ID", "NAZWISKO", "IMIE", "FIRMA", "STANOWISKO", "DZIAL", "MIASTO", "UMOWA", "ID KARTY"]
    entries_width = [5, 5, 15, 15, 25, 47, 21, 22, 26, 16]
    width_count = 0
    for e in entries:
        e = Entry(dict_firma[key], width=entries_width[width_count], justify='center', fg='black')
        e.grid(row=0, column=x) 
        e.insert(END, entries[x])
        x = x + 1
        width_count += 1

dict_firma = {}
def Create_Table(employees):
    i = 1
    place_x = 650
    place_y = 40
    for employee in employees:
        key = str("frame" + str(i))
        dict_firma[key] = Frame(employeesframe)
        dict_firma["canvas" + str(i)] = employeesframe.create_window(place_x, place_y, window=dict_firma[key])
        #dict_firma[key].grid(row=i, column=0)
        entry_width = 5
        e = Entry(dict_firma["frame" + str(i)], width=entry_width, fg='black') 
        e.grid(row=0, column=0) 
        e.insert(END, str(i))
        for j in range(len(employee)):
            if j == 3:
                key = str("firma" + str(i))
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(employee[j])
                firma = dict_firma[key].get()
                e = OptionMenu(dict_firma["frame" + str(i)], dict_firma[key], *firmy, command=lambda firma, employee_id = dict_firma["employee_id" + str(i)].get(): Update_SQL_Data("pracownicy", "firma", firma, "id", employee_id)) 
                e.config(width=18)
                e.grid(row=0, column=j+1)
            elif j == 4:
                key = str("stanowisko" + str(i))
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(employee[j])
                e = OptionMenu(dict_firma["frame" + str(i)], dict_firma[key], *stanowiska, command=lambda stanowisko, employee_id = dict_firma["employee_id" + str(i)].get(): Update_SQL_Data("pracownicy", "stanowisko", stanowisko, "id", employee_id)) 
                e.config(width=40)
                e.grid(row=0, column=j+1)
            elif j == 5:
                key = str("dzial" + str(i))
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(employee[j])
                e = OptionMenu(dict_firma["frame" + str(i)], dict_firma[key], *departments, command=lambda dzial, employee_id = dict_firma["employee_id" + str(i)].get(): Update_SQL_Data("pracownicy", "dzial", dzial, "id", employee_id))
                e.config(width=15)
                e.grid(row=0, column=j+1)
            elif j == 6:
                key = str("miasto" + str(i))
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(employee[j])
                e = OptionMenu(dict_firma["frame" + str(i)], dict_firma[key], *miasta, command=lambda lokalizacja, employee_id = dict_firma["employee_id" + str(i)].get(): Update_SQL_Data("pracownicy", "lokalizacja", lokalizacja, "id", employee_id))
                e.config(width=15)
                e.grid(row=0, column=j+1)
            elif j == 7:
                key = str("umowa" + str(i))
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(employee[j])
                e = OptionMenu(dict_firma["frame" + str(i)], dict_firma[key], *umowy, command=lambda umowa, employee_id = dict_firma["employee_id" + str(i)].get(): Update_SQL_Data("pracownicy", "umowa", umowa, "id", employee_id))
                e.config(width=20)
                e.grid(row=0, column=j+1)
            else:
                if j == 0:
                    entry_width = 5
                    key = "employee_id" + str(i)
                    dict_firma[key] = StringVar(employeesframe)
                    dict_firma[key].set(employee[j])
                elif j == 1:
                    entry_width = 15
                    key = str("employee_name" + str(i))
                    dict_firma[key] = StringVar(employeesframe)
                    dict_firma[key].set(employee[j])
                elif j == 2:
                    entry_width = 15
                    key = "employee_sname" + str(i)
                    dict_firma[key] = StringVar(employeesframe)
                    dict_firma[key].set(employee[j])
                elif j == 8:
                    entry_width == 30
                    key = "card_id" + str(i)
                    dict_firma[key] = StringVar(employeesframe)
                    dict_firma[key].set(employee[j])
                k = j
                e = Entry(dict_firma["frame" + str(i)], width=entry_width, fg='blue') 
                e.grid(row=0, column=j+1)
                e.insert(END, dict_firma[key].get())
        i = i + 1
        place_y += 25
    employeesframe.update()
        
def Print_Employees_By_Department(department):
    employees = get_employees_by_department(department)
    Create_Top_table()
    Create_Table(employees)

def Print_Employees_By_Localization(localization):
    employees = get_employees_by_localization(localization)
    Create_Top_table()
    Create_Table(employees)

def Add_Employee_Window():
    newWindow = Toplevel()
    newWindow.title("Dodawanie pracownika")
    newWindow.geometry("300x250")
    Label(newWindow, text ="#TODO").pack()

def change_password_sql():
    actual_pwd = actual_password.get()
    pwd = password.get()
    pwd2 = password2.get()
    print(actual_pwd)
    print(pwd)
    print(pwd2)

    if pwd != pwd2:
        message.set("Hasla roznia sie od siebie. Sproboj jeszcze raz")
    elif actual_pwd == "" or pwd == "" or pwd2 == "":
        message.set("Uzupelnij prosze wszystkie pola")
    else:
        if validate_login(actual_pwd, pwd) == True:
            #DOSOMETHING
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

select_department = OptionMenu(topframe, department, *departments, command=lambda department:Print_Employees_By_Department(department))
select_department.config(height=2, width=10)
select_department.grid(column=1, row=0, sticky='nw')
select_localization = OptionMenu(topframe, localization, *miasta, command=lambda localization:Print_Employees_By_Localization(localization))
select_localization.config(height=2, width=10)
select_localization.grid(column=2, row=0, sticky='nw')

obecnosc_btn = Button(leftsquare, text="LISTA OBECNOSCI", bg='green', width=20, height=2)
obecnosc_btn.grid(column=3, row=0, sticky='ew')

add_employee_btn = Button(leftframe, text="Dodaj\npracownika", command=lambda: Add_Employee_Window())
add_employee_btn.grid(column=0, row=0, sticky='ew')

add_employee_btn = Button(leftframe, text="Zmien\nhaslo", width=20, command=lambda: Change_Password())
add_employee_btn.grid(column=0, row=1, sticky='ew')

Print_Employees_By_Department("Biuro")

#main_window.withdraw()
main_window.mainloop()