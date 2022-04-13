from tkinter import *

def Create_Occurence_Buttons():
    from pajer import leftframe, leftsquare, employeesframe, employeescanvas, topframe
    select_department = OptionMenu(topframe, department, *departments, command=lambda department:Print_Employees_By_Department(department))
    select_department.config(height=2, width=10)
    select_department.grid(column=1, row=0, sticky='nw')

    select_localization = OptionMenu(topframe, localization, *miasta, command=lambda localization:Print_Employees_By_Localization(localization))
    select_localization.config(height=2, width=10)
    select_localization.grid(column=2, row=0, sticky='nw')

    obecnosc_btn = Button(leftsquare, text="LISTA PRACOWNIKOW", bg='green', width=20, height=2, command=Destroy_Old)
    obecnosc_btn.grid(column=3, row=0, sticky='ew')

    add_employee_btn = Button(leftframe, text="Dodaj\npracownika", command=lambda: Add_Employee_Window())
    add_employee_btn.grid(column=0, row=0, sticky='ew')

    add_employee_btn = Button(leftframe, text="Zmien\nhaslo", width=20, command=lambda: Change_Password())
    add_employee_btn.grid(column=0, row=1, sticky='ew')
