
from login_form.login_form import *
from sql.db_data_functions import *
from windows.pwd import *

login_form()

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
vertibar=Scrollbar(employeescanvas, orient=VERTICAL)
vertibar.pack(side=RIGHT,fill=Y)
vertibar.config(command=employeesframe.yview)
employeesframe.config(width=1300,height=600)
employeesframe.config(yscrollcommand=vertibar.set)
employeesframe.pack(expand=True,side=LEFT)

department = StringVar(main_window)
department.set("Dzial")
localization = StringVar(main_window)
localization.set("Miasto")
dict_firma = {}

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
    employees = get_employees_by_department(department, employeesframe)
    Create_Top_table()
    Create_Table(employees)

def Print_Employees_By_Localization(localization):
    employees = get_employees_by_localization(localization, employeesframe)
    Create_Top_table()
    Create_Table(employees)

def Add_Employee_Window():
    newWindow = Toplevel()
    newWindow.title("Dodawanie pracownika")
    newWindow.geometry("300x250")
    Label(newWindow, text ="#TODO").pack()


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