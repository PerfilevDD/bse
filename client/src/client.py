from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import requests
import asyncio
import websockets
import threading
import json

from PIL import Image, ImageTk
url = "http://localhost:8000"




# LOGIN ------------------------------

def open_login_window():    
    global login_window, entry_name, entry_url, entry_pasword
    login_window = Tk()
    login_window.title("Auth")


    label_name = Label(login_window, text="Name:")
    label_name.grid(row=0, column=0, padx=20, pady=5)
    
    entry_name = Entry(login_window)
    entry_name.grid(row=0, column=1, padx=20, pady=5)
    
    
    label_password = Label(login_window, text="Pass:")
    label_password.grid(row=1, column=0, padx=20, pady=5)
    
    entry_pasword = Entry(login_window)
    entry_pasword.grid(row=1, column=1, padx=20, pady=5)
    
    
    
    label_url = Label(login_window, text="URL:")
    label_url.grid(row=2, column=0, padx=20, pady=5)

    
    entry_url = Entry(login_window)
    entry_url.grid(row=2, column=1, padx=20, pady=5)
    entry_url.insert(0, 'http://localhost:8000')

    button_register = Button(login_window, text="Auth", command=login)
    button_register.grid(row=3, column=1, pady=20)

    login_window.mainloop()



def server_auth_user(name, password):
    try:
        data = {'grant_type': "password", 'username': name, 'password': password}
        r = requests.post(f"{url}/token", data= data)
        r.raise_for_status()
        print(r.json())
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"dd: {e}")
        return None    



def login():  
    global url
    
    name = entry_name.get()
    password = entry_pasword.get()
    
    if not name:        
        messagebox.showwarning("", "Name is required")
        return
    
    if not password:        
        messagebox.showwarning("", "Password is required")
        return
    
    url_label = entry_url.get()
    url = url_label
    
    
    user_data = server_auth_user(name, password)
    
    messagebox.showinfo("test", f"test")
    #login_window.destroy()
    print(user_data)
        
            
open_login_window()