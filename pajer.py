from login_form.login_form import *
from sql.db_data_functions import *
from windows.pwd import *
from datetime import date
from tkcalendar import DateEntry
from pathlib import Path
from tktimepicker import AnalogPicker, AnalogThemes, SpinTimePickerModern, SpinTimePickerOld
from tktimepicker import constants
import requests
import os
from datetime import datetime

version = '0.4.1'
r = requests.get('http://dailystoic.pl/rcp/version.txt', allow_redirects=True)
update_version = str(r.content)[2:-1]
print(update_version)

login_form()
logged_user = ""

try:
    logged_user = uname
except Exception as e:
    print(e)
print(logged_user)

if logged_user != "":
    from queries.rights import *

    sql_query = "SELECT uprawnienia FROM konta WHERE login = '" + logged_user + "'"
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    rights = get_sql.fetchall()[0][0]

    umowy = Get_SQL_Data("_umowa", "rodzaj")
    firmy = Get_SQL_Data("_firma", "firma")
    palacz = Get_SQL_Data("_palacz", "stan")

    akcje = Prepare_SQL_akcje(rights)
    departments = Prepare_SQL_departments(rights)
    stanowiska = Prepare_SQL_stanowiska(rights)
    miasta = Prepare_SQL_miasta(rights)
    teamleaders = Get_SQL_Data("_team", "teamleader")
    teamleaders.append("Nie dotyczy")
    pracownicyzid = Get_SQL_Employees_ID(rights)
    if rights == 777:
        pracownicyzid['PRACOWNIK'] = "*"
        pracownicyzid['WSZYSCY'] = "*"
    elif rights == 5:
        pracownicyzid['SERWIS_ALL'] = "Serwis"
    pracownicybezid = []


    for item in pracownicyzid:
        pracownicybezid.append(item)

    ico_path = str(Path().absolute()) + "\ico\\"
    remove_employee_ico = PhotoImage(file = ico_path + "delete_employee.png")
    remove_entry_ico = PhotoImage(file = ico_path + "remove_entry.png")

    global employeesframe
    global employeescanvas

    topframe = Frame(main_window, width=200)
    topframe.grid(row=0, column=1, sticky='nswe')


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

def Get_Date_From_Callendar(callendar_name):
    dt = callendar_name.get_date()
    str_dt=dt.strftime("%Y-%m-%d")
    #print(str_dt)
    return str_dt

def Generate_Gang_File(window, date1, date2, employee):
    import getpass
    usrname = getpass.getuser()
    destination = f'C:\\Users\\{usrname}\\Documents\\Rejestr_temp.txt'
    destination2 = f'C:\\Users\\{usrname}\\Documents\\Rejestr.txt'
    if employee == "*":
        sql_query = "SELECT obecnosc.time, obecnosc.action, pracownicy.karta FROM obecnosc LEFT JOIN pracownicy ON pracownicy.id = obecnosc.pracownik WHERE obecnosc.time > '" + date1 + " 00:00:01' AND obecnosc.time < '" + date2 + " 23:59:59' AND pracownicy.karta IS NOT NULL"
    else:
        sql_query = "SELECT obecnosc.time, obecnosc.action, pracownicy.karta FROM obecnosc LEFT JOIN pracownicy ON pracownicy.id = obecnosc.pracownik WHERE obecnosc.time > '" + date1 + " 00:00:01' AND obecnosc.time < '" + date2 + " 23:59:59' AND pracownicy.karta IS NOT NULL AND obecnosc.pracownik = " + str(employee)
    print(sql_query)
    try:
        get_sql = conn.cursor()
        get_sql.execute(sql_query)
        sql_result = get_sql.fetchall()
        gang_file = open(destination, 'a+')
        for entry in sql_result:
            gang_cardid = "1" + entry[2][1:]
            gang_date = str(entry[0])
            gang_action = str(entry[1])
            if entry[1] == 1 or entry[1] == 2:
                file_line = gang_cardid + "-" + gang_date[2:] + "-" + gang_action + "\n"
            elif entry[1] in (3, 4, 12, 16, 17, 18, 19):
                print("Omijam wpis " + gang_date + " " + gang_action + " " + gang_cardid)
            else:
                if entry[1] < 10:
                    gang_action = "0" + gang_action
                file_line = gang_cardid + "-" + gang_date[2:11] + "08:00:00-1-" + gang_action + "\n" + gang_cardid + "-" + gang_date[2:11] + "16:00:00-2-" + gang_action + "\n"
            gang_file.write(file_line)
        gang_file.close()

        lines_seen = set() # holds lines already seen
        outfile = open(destination2, "w")
        for line in open(destination, "r"):
            if line not in lines_seen: # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()
        os.remove(destination) 
        window.destroy()
    except Exception as e:
        print(e)
        gng_message.set("Nieokreslony blad")

def Gang_Window():
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")

    newWindow = Toplevel()
    newWindow.title("Generowanie pliku do GANGa")
    newWindow.geometry("350x350")
    global gng_message, employee_input5, data_wpis, data_wpis2
    data_wpis = StringVar()
    data_wpis2 = StringVar()
    employee_input5 = StringVar()
    employee_input5.set("WSZYSCY")
    gng_message = StringVar()
    Label(newWindow, text="Data OD:").place(x=80,y=30)
    calgang1 = DateEntry(newWindow,selectmode='day', width=22, textvariable=data_wpis)
    calgang1.place(x=140,y=30)

    Label(newWindow, text="Data DO:").place(x=80,y=70)
    calgang2 = DateEntry(newWindow,selectmode='day', width=22, textvariable=data_wpis2)
    calgang2.place(x=140,y=70)

    Label(newWindow, text="Pracownik:").place(x=67,y=110)
    OptionMenu(newWindow, employee_input5, *pracownicybezid).place(x=140,y=105)

    Label(newWindow, text="",textvariable=gng_message).place(x=114,y=150)
    Button(newWindow, text="Dodaj wpis", width=15, height=2, bg="orange", command=lambda: Generate_Gang_File(newWindow, Get_Date_From_Callendar(calgang1), Get_Date_From_Callendar(calgang2), pracownicyzid[employee_input5.get()])).place(x=110,y=180)

def Download_Install_Update():
    import subprocess
    #main_window.destroy()
    #uninstall_pajer = '"C:\\Program Files (x86)\\Pajer\\unins000.exe" /VERYSILENT'
    #unistall = subprocess.call(uninstall_pajer, shell=True)
    #print(uninstall_pajer)
    from urllib.request import urlretrieve
    import getpass
    dwn_message.set("Pobrano...")
    url = 'http://dailystoic.pl/rcp/PaJer_install.exe'
    usrname = getpass.getuser()
    destination = f'C:\\Users\\{usrname}\\Downloads\\PaJer_install.exe'
    download = urlretrieve(url, destination)
    returned_value = subprocess.call(destination, shell=True)
    print('returned value:', returned_value)
    sys.exit()

def Actualization_Window(version, webversion):
    newWindow = Toplevel()
    newWindow.title("Aktualizacja")
    newWindow.geometry("300x100")
    if version == webversion:
        Label(newWindow, text="Wszystko jest aktualne :)", font='Helvetica 14 bold').place(x=40,y=20)
        Button(newWindow, text="OK :D", width=10, height=1, bg="green", command= lambda:newWindow.destroy()).place(x=105,y=60 )
    else:
        global dwn_message
        dwn_message = StringVar()
        Label(newWindow, text="", textvariable=dwn_message).place(x=800,y=80)
        Button(newWindow, text="Pobierz aktualizacje", width=15, height=2, bg="orange", command = lambda: Download_Install_Update()).place(x=95,y=30)

def Are_You_Sure_Button(value, frame, case):
    are_you_sure = Toplevel()
    are_you_sure.title("Potwierdz wybor")
    are_you_sure.geometry("200x200")
    if case == 1:
        employee = Get_Single_SQL_Data("pracownicy", "imie", value) + " " + Get_Single_SQL_Data("pracownicy", "nazwisko", value)
        Label(are_you_sure, text="Czy na pewno chcesz usunac:\n" + employee).place(x=20,y=30)
        table_name = "pracownicy"
    elif case == 2:
        table_name = "obecnosc"
        Label(are_you_sure, text="Czy na pewno chcesz usunac wpis?").place(x=2,y=30)

    Button(are_you_sure, text="Tak", width=10, height=1, bg="orange",command=lambda table_name=table_name, frame=frame, value=value: [Remove_SQL_Data(table_name, "id", value), frame.destroy(), are_you_sure.destroy(), employeesframe.update()]).place(x=65,y=90)
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
            if rights == 777:
                key = str("dzial" + str(i))
                dict_firma[key] = StringVar(employeesframe)
                dict_firma[key].set(employee[j])
                e = Button(dict_firma["frame" + str(i)], text = "Usun", image=remove_employee_ico, command=lambda frame = dict_firma[str("frame" + str(i))], employee_id = dict_firma["employee_id" + str(i)].get(): Are_You_Sure_Button(employee_id, frame, 1))
                e.grid(row=0, column=10)
        i = i + 1
        place_y += 25
    #employeesframe.update()
        
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
                e = Button(dict_firma["frame" + str(i)], text = "Usun", image=remove_entry_ico, command=lambda frame = dict_firma[str("frame" + str(i))], employee_id = dict_firma["employee_db_id" + str(i)].get(): Are_You_Sure_Button(employee_id, frame, 2))
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

def Add_Employee_button(window):
    fname=first_name.get()
    sname=second_name.get()
    dprm=emp_department.get()
    smk=smoker.get()
    lclz=emp_localiziation.get()
    tmld=teamleader.get()
    crdi=emp_card_id.get()
    arng=arrangement.get()
    cmpy=company.get()
    pst=position.get()
    #applying empty validation
    if fname == '' or sname == '' or dprm == 'DZIAL' or smk == 'NIE/TAK' or lclz == "MIASTO" or tmld == "TEAMLEADER" or crdi == "" or arng == "UMOWA" or cmpy == "FIRMA" or pst == "STANOWISKO":
        emp_message.set("Uzupelnij wszystkie pola!")
    else:
        dprm = Get_SQL_Data_ForUpdate("_dzial", "dzial", dprm)
        smk = Get_SQL_Data_ForUpdate("_palacz", "stan", smk)
        lclz = Get_SQL_Data_ForUpdate("_lokalizacja", "miasto", lclz)
        if tmld == "Nie dotyczy":
            tmld = "NULL"
        else:
            tmld = Get_SQL_Data_ForUpdate("_team", "teamleader", tmld)
        arng = Get_SQL_Data_ForUpdate("_umowa", "rodzaj", arng)
        cmpy = Get_SQL_Data_ForUpdate("_firma", "firma", cmpy)
        pst = Get_SQL_Data_ForUpdate("_stanowisko", "stanowisko", pst)
        sql_query_addemployee = "INSERT INTO pracownicy (imie, nazwisko, palacz, dzial, lokalizacja, teamleader, karta, umowa, firma, stanowisko) VALUES ('"+fname+"','"+sname+"',"+str(smk)+","+str(dprm)+","+str(lclz)+","+str(tmld)+",'"+str(crdi)+"',"+str(arng)+","+str(cmpy)+","+str(pst)+");"
        print(tmld)
        Update_SQL_Data_Prepared(sql_query_addemployee)
        window.destroy()
        employeesframe.update()

def Add_Entry_button(window, date):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print(dt_string)
    akcja = ent_akcja.get()
    if akcja == 'RODZAJ WPISU' or employee_input5.get() == "PRACOWNIK" or employee_input5.get() == "SERWIS_ALL":
        emp_message.set("Uzupelnij wszystkie pola!")
    else:
        koment = comment.get()
        employee_entry = pracownicyzid[employee_input5.get()]
        time = time_picker.time()
        time_str = ["07", "00"]
        if time[0] < 10:
            time_str[0] = "0" + str(time[0])
        else:
            time_str[0] = str(time[0])
        if time[1] < 10:
            time_str[1] = "0" + str(time[1])
        else:
            time_str[1] = str(time[1])
        time = " " + time_str[0] + ":" + time_str[1] + ":00"
        acti = Get_SQL_Data_ForUpdate("_action", "action", akcja)
        sql_query = "INSERT INTO obecnosc (pracownik, time, action, komentarz, edit, edit_time) VALUES ('" + str(employee_entry) + "', '" + date + time + "', '" + str(acti) + "', '" + koment + "', '" + logged_user + "', '" + dt_string + "')"
        Update_SQL_Data_Prepared(sql_query)
        window.destroy()

def Add_Comment_button(window, date):
    employee_entry = pracownicyzid[employee_input5.get()]
    koment = comment.get()
    if employee_entry == '*' or koment == '':
        emp_message.set("Uzupelnij wszystkie pola!")
    else:
        sql_query = "SELECT id from obecnosc WHERE pracownik = " + str(employee_entry) + " AND action = 1 AND time LIKE '" + date + "%'"
        print(sql_query)
        try:
            get_sql = conn.cursor()
            get_sql.execute(sql_query)
            sql_result = get_sql.fetchall()[0][0]
            update_sql = "UPDATE obecnosc SET komentarz = '" + koment + "' WHERE id = " + str(sql_result)
            print(update_sql)
            get_sql.execute(update_sql)
            conn.commit()
            window.destroy()
        except:
            emp_message.set("Prawdopodobnie brak wpisu")

def Add_Comment_Window():
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")

    newWindow = Toplevel()
    newWindow.title("Dodawanie komentarza")
    newWindow.geometry("350x350")
    global emp_message, employee_input5, data_wpis, comment
    comment = StringVar()
    data_wpis = StringVar()
    employee_input5 = StringVar()
    employee_input5.set(employee_input.get())
    emp_message = StringVar()

    Label(newWindow, text="Data:").place(x=100,y=30)
    cal2 = DateEntry(newWindow,selectmode='day', width=22, textvariable=data_wpis)
    cal2.place(x=140,y=30)

    Label(newWindow, text="Pracownik:").place(x=67,y=80)
    OptionMenu(newWindow, employee_input5, *pracownicybezid).place(x=140,y=76)

    Label(newWindow, text="Komentarz:").place(x=68,y=130)
    Entry(newWindow, textvariable=comment).place(x=140,y=130)

    Label(newWindow, text="",textvariable=emp_message).place(x=105,y=160)
    Button(newWindow, text="Dodaj wpis", width=15, height=2, bg="orange",command=lambda: Add_Comment_button(newWindow, Get_Date_From_Callendar(cal2))).place(x=110,y=190)

def Add_Entry_Window():
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")

    newWindow = Toplevel()
    newWindow.title("Dodawanie wpisu")
    newWindow.geometry("350x350")
    global ent_akcja, emp_message, employee_input5, data_wpis, comment, time_picker
    comment = StringVar()
    data_wpis = StringVar()
    employee_input5 = StringVar()
    employee_input5.set(employee_input.get())
    ent_akcja = StringVar()
    ent_akcja.set("RODZAJ WPISU")
    emp_message = StringVar()

    Label(newWindow, text="Data:").place(x=120,y=30)
    cal2 = DateEntry(newWindow,selectmode='day', width=22, textvariable=data_wpis)
    cal2.place(x=160,y=30)

    Label(newWindow, text="Czas:").place(x=120,y=74)
    time_picker = SpinTimePickerModern(newWindow)
    time_picker.addAll(constants.HOURS24)
    time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040", hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
    time_picker.configure_separator(bg="#404040", fg="#ffffff")
    time_picker.place(x=160,y=70)

    Label(newWindow, text="Rodzaj wpisu:").place(x=77,y=114)
    OptionMenu(newWindow, ent_akcja, *akcje).place(x=160,y=110)

    Label(newWindow, text="Pracownik:").place(x=87,y=150)
    OptionMenu(newWindow, employee_input5, *pracownicybezid).place(x=160,y=150)

    Label(newWindow, text="Komentarz:").place(x=88,y=195)
    Entry(newWindow, textvariable=comment).place(x=160,y=195)

    Label(newWindow, text="",textvariable=emp_message).place(x=134,y=240)
    Button(newWindow, text="Dodaj wpis", width=15, height=2, bg="orange",command=lambda: Add_Entry_button(newWindow, Get_Date_From_Callendar(cal2))).place(x=130,y=270)

def Add_Employee_Window():
    print(uname)
    newWindow = Toplevel()
    newWindow.title("Dodawanie pracownika")
    newWindow.geometry("500x350")
    global first_name, second_name, smoker, emp_department, emp_localiziation, teamleader, emp_card_id, arrangement, company, position, emp_message
    first_name  = StringVar()
    second_name = StringVar()
    smoker = StringVar()
    smoker.set("NIE/TAK")
    emp_department = StringVar()
    emp_department.set("DZIAL")
    emp_localiziation = StringVar()
    emp_localiziation.set("MIASTO")
    teamleader = StringVar()
    teamleader.set("TEAMLEADER")
    emp_card_id = StringVar()
    arrangement = StringVar()
    arrangement.set("UMOWA")
    company = StringVar()
    company.set("FIRMA")
    position = StringVar()
    position.set("STANOWISKO")
    emp_message = StringVar()

    Label(newWindow, text="Imie:").place(x=40,y=30)
    Entry(newWindow, textvariable=first_name).place(x=80,y=30)

    Label(newWindow, text="Nazwisko:").place(x=220,y=30)
    Entry(newWindow, textvariable=second_name).place(x=290,y=30)

    Label(newWindow, text="Palacz:").place(x=34,y=70)
    OptionMenu(newWindow, smoker, *palacz).place(x=80,y=66)

    Label(newWindow, text="Dzial:").place(x=220,y=70)
    OptionMenu(newWindow, emp_department, *departments).place(x=290,y=66)

    Label(newWindow, text="Lokalizacja:").place(x=15,y=110)
    OptionMenu(newWindow, emp_localiziation, *miasta).place(x=80,y=106)

    Label(newWindow, text="TeamLeader:").place(x=220,y=110)
    OptionMenu(newWindow, teamleader, *teamleaders).place(x=290,y=106)

    Label(newWindow, text="ID karty:").place(x=27,y=150)
    Entry(newWindow, textvariable=emp_card_id).place(x=80,y=150)

    Label(newWindow, text="Umowa:").place(x=220,y=150)
    OptionMenu(newWindow, arrangement, *umowy).place(x=290,y=146)

    Label(newWindow, text="Firma:").place(x=35,y=190)
    OptionMenu(newWindow, company, *firmy).place(x=80,y=186)

    Label(newWindow, text="Stanowisko:").place(x=220,y=190)
    OptionMenu(newWindow, position, *stanowiska).place(x=290,y=186)

    Label(newWindow, text="",textvariable=emp_message).place(x=174,y=240)
    Button(newWindow, text="Dodaj pracownika", width=15, height=2, bg="orange",command=lambda: Add_Employee_button(newWindow)).place(x=180,y=270)

def clear(frame_name):
    list = frame_name.grid_slaves()
    for l in list:
        l.destroy()

def Destroy_Old():
    clear(topframe)
    clear(leftframe)
    clear(leftsquare)

def Print_Occurance(input_type, input_value, input_value_2, employee_input):
    print(input_type)
    print(input_value)
    if input_type == 1:
        occurance = get_occurence_by_entry_time(input_value, employeesframe)
    elif input_type == 2:
        occurance = get_occurence_by_entry_time_two(input_value, input_value_2, employee_input, employeesframe)
    Create_Top_table_occurance()
    Create_Table_Occurance(occurance)

def Create_Employee_Tab():
    Destroy_Old()
    employeesframe.update()
    select_1 = OptionMenu(topframe, department, *departments, command=lambda department:Print_Employees_By_Department(department))
    select_1.config(height=2, width=10)
    select_1.grid(column=1, row=0, sticky='nw')

    if rights != 5:
        select_2 = OptionMenu(topframe, localization, *miasta, command=lambda localization:Print_Employees_By_Localization(localization))
        select_2.config(height=2, width=10)
        select_2.grid(column=2, row=0, sticky='nw')

    obecnosc_btn = Button(leftsquare, text="LISTA OBECNOSCI", bg='green', width=20, height=2, command=Create_Occurance_Tab)
    obecnosc_btn.grid(column=3, row=0, sticky='ew')

    btn_1 = Button(leftframe, text="Dodaj\npracownika", width=20, command=lambda: Add_Employee_Window())
    btn_1.grid(column=0, row=0, sticky='ew')

    btn_2 = Button(leftframe, text="Zmien\nhaslo", width=20, command=lambda: Change_Password())
    btn_2.grid(column=0, row=1, sticky='ew')

    actu_btn = Button(main_window, text="Sprawdz\naktualizacje", width=10, height=2, command=lambda: Actualization_Window(version, update_version))
    actu_btn.grid(column=2, row=0, sticky='e')

def Create_Occurance_Tab():
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    Destroy_Old()
    occurance = get_occurence_by_entry_time(d1, employeesframe)
    Create_Top_table_occurance()
    Create_Table_Occurance(occurance)
    global date_input
    date_input=StringVar()
    global date_input_2
    date_input_2=StringVar()
    global select_1
    global select_2
    global employee_input
    employee_input=StringVar()
    employee_input.set("PRACOWNIK")

    label_1 = Label(topframe, text="OD:").grid(column=0, row=0)
    label_2 = Label(topframe, text="DO:").grid(column=0, row=1)

    select_1 = DateEntry(topframe,selectmode='day', width=22, textvariable=date_input)
    select_1.grid(column=1, row=0, sticky='nw')
    select_2 = DateEntry(topframe,selectmode='day', width=22, textvariable=date_input_2)
    select_2.grid(column=1, row=1, sticky='nw')

    opt_1 = OptionMenu(topframe, employee_input, *pracownicybezid).grid(column=2, row=0)

    btn_2 = Button(topframe, text="Odswiez", width=10, command=lambda: Print_Occurance(2, Get_Date_From_Callendar(select_1), Get_Date_From_Callendar(select_2), pracownicyzid[employee_input.get()]))
    btn_2.grid(column=2, row=1, sticky='ew')

    btn_1 = Button(leftframe, text="Dodaj\nwpis", width=20, command=lambda: Add_Entry_Window())
    btn_1.grid(column=0, row=0, sticky='ew')

    btn_3 = Button(leftframe, text="Dodaj\nkomentarz", width=20, command=lambda: Add_Comment_Window())
    btn_3.grid(column=0, row=1, sticky='ew')

    obecnosc_btn = Button(leftsquare, text="LISTA PRACOWNIKOW", bg='green', width=20, height=2, command=Create_Employee_Tab)
    obecnosc_btn.grid(column=3, row=0, sticky='ew')

    actu_btn = Button(main_window, text="Sprawdz\naktualizacje", width=10, height=2, command=lambda: Actualization_Window(version, update_version))
    actu_btn.grid(column=2, row=0, sticky='e')

    gang_btn = Button(main_window, text="Generuj plik\nWapro GANG", width=10, height=2, comman=lambda: Gang_Window())
    gang_btn.grid(column=2, row=1, sticky='n')




    


#select_1 = OptionMenu(topframe, department, *departments, command=lambda department:Print_Employees_By_Department(department))
#select_1.config(height=2, width=10)
#select_1.grid(column=1, row=0, sticky='nw')

#select_2 = OptionMenu(topframe, localization, *miasta, command=lambda localization:Print_Employees_By_Localization(localization))
#select_2.config(height=2, width=10)
#select_2.grid(column=2, row=0, sticky='nw')

#obecnosc_btn = Button(leftsquare, text="LISTA OBECNOSCI", bg='green', width=20, height=2, command=Create_Occurance_Tab)
#obecnosc_btn.grid(column=3, row=0, sticky='ew')

#btn_1 = Button(leftframe, text="Dodaj\npracownika", width=20, command=lambda: Add_Employee_Window())
#btn_1.grid(column=0, row=0, sticky='ew')

#btn_2 = Button(leftframe, text="Zmien\nhaslo", width=20, command=lambda: Change_Password())
#btn_2.grid(column=0, row=1, sticky='ew')




#actu_btn = Button(main_window, text="Sprawdz\naktualizacje", width=10, height=2, command=lambda: Actualization_Window(version, update_version))
#actu_btn.grid(column=2, row=0, sticky='n')





try:
    print(uname)
    #login_screen.destroy()
    if rights == 5:
        Print_Employees_By_Department("Serwis")
    else:
        Print_Employees_By_Department("Biuro")
except:
    print("Nie ma mnie")
    main_window.withdraw()
    main_window.mainloop()