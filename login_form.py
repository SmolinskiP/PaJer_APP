
from tkinter import *
from validate_login import validate_login
import sys

def login():
    uname=username.get()
    pwd=password.get()
    #applying empty validation
    if uname=='' or pwd=='':
        message.set("Wpisz prosze login i haslo")
    else:
        if validate_login(uname, pwd) == True:
            main_window.deiconify()
            login_screen.destroy()
        else:
            message.set("Wrong username or password!!!")

def login_form():
    global login_screen
    login_screen = Toplevel()
    login_screen.title("Logowanie")
    login_screen.geometry("300x250")

    #declaring variable
    global message;
    global username
    global password
    username = StringVar()
    password = StringVar()
    message=StringVar()

    Label(login_screen,width="300", text="Please enter details below", bg="orange",fg="white").pack()
    Label(login_screen, text="Username * ").place(x=20,y=40)
    Entry(login_screen, textvariable=username).place(x=90,y=42)
    Label(login_screen, text="Password * ").place(x=20,y=80)
    Entry(login_screen, textvariable=password ,show="*").place(x=90,y=82)
    Label(login_screen, text="",textvariable=message).place(x=95,y=100)

    Button(login_screen, text="Login", width=10, height=1, bg="orange",command=login).place(x=105,y=130)


main_window = Tk()
main_window.title("PaJer - najlepszy program Rejestracji Czasu Pracy we wszechswiecie")