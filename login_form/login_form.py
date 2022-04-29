from tkinter import *

def refresh(self):
    self.destroy()
    self.__init__()


def login():
    global uname
    uname=username.get()
    pwd=password.get()
    #applying empty validation
    if uname=='' or pwd=='':
        message.set("Wpisz prosze login i haslo")
    else:
        from windows.pwd import validate_login
        if validate_login(uname, pwd) == True:
            main_window.deiconify()
            login_screen.destroy()
            from pajer import Create_Employee_Tab
            Create_Employee_Tab()
        else:
            message.set("Wrong username or password!!!")

def login_form():
    global login_screen
    try:
        print(uname)
    except:
        login_screen = Toplevel()
        login_screen.title("Logowanie")
        login_screen.geometry("300x250")

    #declaring variable
        global message;
        global username
        global password
        username = StringVar()
        password = StringVar()
        message = StringVar()

        Label(login_screen,width="300", text="Wpisz swoj login i haslo", bg="orange",fg="white").pack()
        Label(login_screen, text="Username * ").place(x=20,y=40)
        Entry(login_screen, textvariable=username).place(x=90,y=42)
        Label(login_screen, text="Password * ").place(x=20,y=80)
        Entry(login_screen, textvariable=password ,show="*").place(x=90,y=82)
        Label(login_screen, text="",textvariable=message).place(x=95,y=100)

        Button(login_screen, text="Login", width=10, height=1, bg="orange",command=login).place(x=105,y=130)


    #login_screen.destroy()


main_window = Tk()
main_window.title("PaJer v0.6.2 - najlepszy program Rejestracji Czasu Pracy we wszechswiecie")