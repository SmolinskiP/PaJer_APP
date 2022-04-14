from login_form.login_form import *
from sql.db_data_functions import *
from windows.pwd import *
from datetime import date
from tkcalendar import DateEntry
from pathlib import Path

login_form()

umowy = Get_SQL_Data("_umowa", "rodzaj")
departments = Get_SQL_Data("_dzial", "dzial")
stanowiska = Get_SQL_Data("_stanowisko", "stanowisko")
firmy = Get_SQL_Data("_firma", "firma")
miasta = Get_SQL_Data("_lokalizacja", "miasto")

ico_path = str(Path().absolute()) + "\ico\delete_employee.png"
remove_employee_ico = PhotoImage(file = ico_path)

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

def Are_You_Sure_Button(value, frame, case):
    are_you_sure = Toplevel()
    are_you_sure.title("Potwierdz wybor")
    are_you_sure.geometry("200x200")
    if case == 1:
        employee = Get_Single_SQL_Data("pracownicy", "imie", value) + " " + Get_Single_SQL_Data("pracownicy", "nazwisko", value)
        Label(are_you_sure, text="Czy na pewno chcesz usunac:\n" + employee).place(x=20,y=30)
    elif case == 2:
        Label(are_you_sure, text="Czy na pewno chcesz usunac wpis?").place(x=2,y=30)

    Button(are_you_sure, text="Tak", width=10, height=1, bg="orange",command=lambda frame=frame, value=value: [Remove_SQL_Data("pracownicy", "id", value), frame.destroy(), are_you_sure.destroy()]).place(x=65,y=90)
    Button(are_you_sure, text="Nie", width=10, height=1, bg="orange",command=are_you_sure.destroy).place(x=65,y=130)

def Create_Top_table():
    key = "topframe"
    dict_firma[key] = Frame(employeesframe)
    canvas_toplabel = employeesframe.create_window(650, 20, window=dict_firma[key])
    #dict_firma[key].grid(row=0, column=0)
    x = 0
    entries = ["LP", "ID", "NAZWISKO", "IMIE", "FIRMA", "STANOWISKO", "DZIAL", "MIASTO", "UMOWA", "ID KARTY"]
    entries_width = [5, 5, 15, 15, 25, 47, 21, 22, 26, 20]
    width_count = 0
    for e in entries:
        e = Entry(dict_firma[key], width=entries_width[width_count], justify='center', fg='black')
        e.grid(row=0, column=x) 
        e.insert(END, entries[x])
        x = x + 1
        width_count += 1

def Create_Top_table_occurance():
    key = "topframe"
    dict_firma[key] = Frame(employeesframe)
    canvas_toplabel = employeesframe.create_window(650, 20, window=dict_firma[key])
    #dict_firma[key].grid(row=0, column=0)
    x = 0
    entries = ["LP", "ID", "NAZWISKO", "IMIE", "CZAS", "AKCJA", "KOMENTARZ", "ID_WPIS"]
    entries_width = [5, 5, 15, 15, 25, 40, 90, 14]
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
            key = str("dzial" + str(i))
            dict_firma[key] = StringVar(employeesframe)
            dict_firma[key].set(employee[j])
            e = Button(dict_firma["frame" + str(i)], text = "Usun", image=remove_employee_ico, command=lambda frame = dict_firma[str("frame" + str(i))], employee_id = dict_firma["employee_id" + str(i)].get(): Are_You_Sure_Button(employee_id, frame, 1))
            e.grid(row=0, column=10)
        i = i + 1
        place_y += 25
    employeesframe.update()
        
def Create_Table_Occurance(occurance):
    i = 1
    place_x = 650
    place_y = 40
    for event in occurance:
        key = str("frame" + str(i))
        dict_firma[key] = Frame(employeesframe)
        dict_firma["canvas" + str(i)] = employeesframe.create_window(place_x, place_y, window=dict_firma[key])
        #dict_firma[key].grid(row=i, column=0)
        entry_width = 5
        e = Entry(dict_firma["frame" + str(i)], width=entry_width, fg='black') 
        e.grid(row=0, column=0) 
        e.insert(END, str(i))
        for j in range(len(event)):
            if j == 0:
                entry_width = 5
                key = "employee_ocu_id" + str(i)
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(event[j])
                k = j
                e = Entry(dict_firma["frame" + str(i)], width=entry_width, fg='blue') 
                e.grid(row=0, column=j+1)
                e.insert(END, dict_firma[key].get())
            elif j == 1:
                entry_width = 15
                key = "employee_ocu_sname" + str(i)
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(event[j])
                k = j
                e = Entry(dict_firma["frame" + str(i)], width=entry_width, fg='blue') 
                e.grid(row=0, column=j+1)
                e.insert(END, dict_firma[key].get())
            elif j == 2:
                entry_width = 15
                key = "employee_ocu_name" + str(i)
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(event[j])
                k = j
                e = Entry(dict_firma["frame" + str(i)], width=entry_width, fg='blue') 
                e.grid(row=0, column=j+1)
                e.insert(END, dict_firma[key].get())
            elif j == 3:
                entry_width = 25
                key = "employee_time" + str(i)
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(event[j])
                k = j
                e = Entry(dict_firma["frame" + str(i)], width=entry_width, fg='blue') 
                e.grid(row=0, column=j+1)
                e.insert(END, dict_firma[key].get())
            elif j == 4:
                entry_width = 40
                key = "employee_action" + str(i)
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(event[j])
                k = j
                e = Entry(dict_firma["frame" + str(i)], width=entry_width, fg='blue') 
                e.grid(row=0, column=j+1)
                e.insert(END, dict_firma[key].get())
            elif j == 5:
                entry_width = 90
                key = "employee_comment" + str(i)
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(event[j])
                k = j
                e = Entry(dict_firma["frame" + str(i)], width=entry_width, fg='blue') 
                e.grid(row=0, column=j+1)
                e.insert(END, dict_firma[key].get())
            elif j == 6:
                entry_width = 10
                key = "employee_db_id" + str(i)
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(event[j])
                k = j
                e = Entry(dict_firma["frame" + str(i)], width=entry_width, fg='blue') 
                e.grid(row=0, column=j+1)
                e.insert(END, dict_firma[key].get())
                key = str("rm_btn" + str(i))
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(event[j])
                e = Button(dict_firma["frame" + str(i)], text = "Usun", image=remove_employee_ico, command=lambda frame = dict_firma[str("frame" + str(i))], employee_id = dict_firma["employee_db_id" + str(i)].get(): Are_You_Sure_Button(employee_id, frame, 2))
                e.grid(row=0, column=8)
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

def clear(frame_name):
    list = frame_name.grid_slaves()
    for l in list:
        l.destroy()

def Destroy_Old():
    clear(topframe)
    clear(leftframe)
    clear(leftsquare)

def Get_Date_From_Callendar():
    dt = select_1.get_date()
    str_dt=dt.strftime("%Y-%m-%d")
    return str_dt

def Print_Occurance(input_type, input_value):
    if input_type == 1:
        occurance = get_occurence_by_entry_time(input_value, employeesframe)
    Create_Top_table_occurance()
    Create_Table_Occurance(occurance)

def Create_Employee_Tab():
    Destroy_Old()
    employeesframe.update()
    select_1 = OptionMenu(topframe, department, *departments, command=lambda department:Print_Employees_By_Department(department))
    select_1.config(height=2, width=10)
    select_1.grid(column=1, row=0, sticky='nw')

    select_2 = OptionMenu(topframe, localization, *miasta, command=lambda localization:Print_Employees_By_Localization(localization))
    select_2.config(height=2, width=10)
    select_2.grid(column=2, row=0, sticky='nw')

    obecnosc_btn = Button(leftsquare, text="LISTA OBECNOSCI", bg='green', width=20, height=2, command=Create_Occurance_Tab)
    obecnosc_btn.grid(column=3, row=0, sticky='ew')

    btn_1 = Button(leftframe, text="Dodaj\npracownika", width=20, command=lambda: Add_Employee_Window())
    btn_1.grid(column=0, row=0, sticky='ew')

    btn_2 = Button(leftframe, text="Zmien\nhaslo", width=20, command=lambda: Change_Password())
    btn_2.grid(column=0, row=1, sticky='ew')

def Create_Occurance_Tab():
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    Destroy_Old()
    occurance = get_occurence_by_entry_time(d1, employeesframe)
    Create_Top_table_occurance()
    Create_Table_Occurance(occurance)
    global date_input
    date_input=StringVar()
    global select_1
    select_1 = DateEntry(topframe,selectmode='day', width=22, textvariable=date_input)
    select_1.grid(column=1, row=0, sticky='nw')

    btn_2 = Button(topframe, text="Odswiez", width=20, command=lambda: Print_Occurance(1, Get_Date_From_Callendar()))
    btn_2.grid(column=1, row=2, sticky='ew')

    obecnosc_btn = Button(leftsquare, text="LISTA PRACOWNIKOW", bg='green', width=20, height=2, command=Create_Employee_Tab)
    obecnosc_btn.grid(column=3, row=0, sticky='ew')



    


select_1 = OptionMenu(topframe, department, *departments, command=lambda department:Print_Employees_By_Department(department))
select_1.config(height=2, width=10)
select_1.grid(column=1, row=0, sticky='nw')

select_2 = OptionMenu(topframe, localization, *miasta, command=lambda localization:Print_Employees_By_Localization(localization))
select_2.config(height=2, width=10)
select_2.grid(column=2, row=0, sticky='nw')

obecnosc_btn = Button(leftsquare, text="LISTA OBECNOSCI", bg='green', width=20, height=2, command=Create_Occurance_Tab)
obecnosc_btn.grid(column=3, row=0, sticky='ew')

btn_1 = Button(leftframe, text="Dodaj\npracownika", width=20, command=lambda: Add_Employee_Window())
btn_1.grid(column=0, row=0, sticky='ew')

btn_2 = Button(leftframe, text="Zmien\nhaslo", width=20, command=lambda: Change_Password())
btn_2.grid(column=0, row=1, sticky='ew')

Print_Employees_By_Department("Biuro")

#main_window.withdraw()
main_window.mainloop()