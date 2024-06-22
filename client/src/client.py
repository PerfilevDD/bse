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
token = ''




# AUTHETIFICATION ------------------------------

def open_login_window():    
    global login_window, entry_name, entry_url, entry_pasword
    login_window = Tk()
    login_window.title("Auth")

    # Email
    label_name = Label(login_window, text="E-Mail:")
    label_name.grid(row=0, column=0, padx=20, pady=5)
    
    entry_name = Entry(login_window)
    entry_name.grid(row=0, column=1, padx=20, pady=5)
    
    # Pass
    label_password = Label(login_window, text="Pass:")
    label_password.grid(row=1, column=0, padx=20, pady=5)
    
    entry_pasword = Entry(login_window)
    entry_pasword.grid(row=1, column=1, padx=20, pady=5)
    
    
    # URL
    label_url = Label(login_window, text="URL:")
    label_url.grid(row=2, column=0, padx=20, pady=5)

    
    entry_url = Entry(login_window)
    entry_url.grid(row=2, column=1, padx=20, pady=5)
    entry_url.insert(0, 'http://localhost:8000')
    
    # Buttons
    button_reg = Button(login_window, text="Reg", command=registrarion)
    button_reg.grid(row=3, column=0, pady=20)

    button_login = Button(login_window, text="Login", command=login)
    button_login.grid(row=3, column=1, pady=20)

    login_window.mainloop()



# Login
def server_auth_user(email, password):
    global token
    try:
        data = {'grant_type': "password", 'username': email, 'password': password}
        r = requests.post(f"{url}/token", data = data)
        r.raise_for_status()
        token = r.json()['access_token']
        print(f"token: {token}")
        return r.json()
    except requests.exceptions.RequestException as e:
        try:
            return r.json()['detail']  
        except:
            return None  

def login():  
    global url
    
    email = entry_name.get()
    password = entry_pasword.get()
    
    if not email:        
        messagebox.showwarning("", "Name is required")
        return
    
    if not password:        
        messagebox.showwarning("", "Password is required")
        return
    
    url_label = entry_url.get()
    url = url_label
    
    
    user_data = server_auth_user(email, password)
    
    print(token)
    if token != '':
        messagebox.showinfo("", f"Wellcome")
        #login_window.destroy()
    elif user_data == "Incorrect email or password":
        messagebox.showinfo("", f"{user_data}")
    elif user_data == "user in nor register":
        messagebox.showinfo("", f"You need to register")
    else:
        messagebox.showinfo("", f"No Internet!")
        
        
        


# Registrarion

def registrarion():
    global url
    
    email = entry_name.get()
    password = entry_pasword.get()
    
    if not email:        
        messagebox.showwarning("", "Name is required")
        return
    
    if not password:        
        messagebox.showwarning("", "Password is required")
        return
    
    url_label = entry_url.get()
    url = url_label
    
    try:
        data = {'email': email, 'password': password}
        r = requests.post(f"{url}/register", json = data)
        r.raise_for_status()
        if r.json()['status'] == 'reg complete':
            server_auth_user(email, password)
            messagebox.showinfo("", f"Wellcome")
            #login_window.destroy()
            return r.json()
        else:
            messagebox.showinfo("", f"User alredy existes")
    except requests.exceptions.RequestException as e:
        messagebox.showinfo("", f"No Internet!")
        return None  
    
    


# MAINWINDOW ------------------------------
        
        
            
open_login_window()