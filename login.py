
from login_form import *
from tkinter import *
import tkinter as tk
from tkinter import *
import mysql.connector as database
from db_connect import *

login_form()

department = StringVar(main_window)
department.set("Kadry")
departments = ("Kadry", "Biuro")

try:
    conn = database.connect(user = dbLogin, password = dbPassword, host = dbHost, database = dbDatabase)
except database.Error as e:
    print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")

def get_employees_by_department(department):
        get_employees = conn.cursor()
        get_employees.execute("SELECT employees.fname, employees.lname, employees.login, _department.department FROM employees JOIN _department ON employees.department = _department.id WHERE _department.department = '%s'" % department)
        employees = get_employees.fetchall()
        i = 0
        for employee in employees:
            for j in range(len(employee)):
                e = Entry(main_window, width=10, fg='blue') 
                e.grid(row=i+1, column=j+1) 
                e.insert(END, employee[j])
            i = i + 1
            main_window.update()

employees_department_1 = tk.Button(main_window,text="Demo Button", command=lambda:get_employees_by_department("Kadry"))
employees_department_1.grid(row=0, column=0)

employees_department_2 = tk.Button(main_window,text="Demo Button", command=lambda:get_employees_by_department("Biuro"))
employees_department_2.grid(row=0, column=1)

select_department = OptionMenu(main_window, department, *departments, command=lambda department:get_employees_by_department(department))
select_department.grid(column=0, row=1)

#main_window.withdraw()
main_window.mainloop()