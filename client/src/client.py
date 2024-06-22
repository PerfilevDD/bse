from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import requests
import asyncio
import websockets
import threading
import json

from ttkbootstrap import Style

from PIL import Image, ImageTk
url = "http://localhost:8000"
token = ''
user_id = 0;




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

def buy_func(feet_price, feet_amount):
    global url
    
    price = feet_price.get()
    amount = feet_amount.get()
    
    try:
        data = {'trader_id': user_id, 'item': 'frc','pair_item': 'poc', 'price': price, 'item_amount': amount}
        r = requests.post(f"{url}/trade", json = data)
        r.raise_for_status()
        r.json()['status'] == 'trade reg complete'
            
        messagebox.showinfo("", f"comlete")
        return r.json()
    
    except requests.exceptions.RequestException as e:
        messagebox.showinfo("", f"No Internet!")
        return None  
    
    
def sell_func(feet_price, feet_amount):
    global url
    
    price = feet_price.get()
    amount = feet_amount.get()
    
    try:
        data = {'trader_id': user_id, 'item': 'poc','pair_item': 'frc', 'price': price, 'item_amount': amount}
        r = requests.post(f"{url}/trade", json = data)
        r.raise_for_status()
        r.json()['status'] == 'trade reg complete'
            
        messagebox.showinfo("", f"comlete")
        return r.json()
    
    except requests.exceptions.RequestException as e:
        messagebox.showinfo("", f"No Internet!")
        return None  
    

    
def open_game_window():
    global root, entry_price, entry_amount
    
    # Main window
    root = Tk()
    root.title("Bonn Stock Exchange")
    
    # Style settings
    style = Style('darkly')


    # Window settings
    mainframe = ttk.Frame(root, padding="70 70 70 70")
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # BUY_______________________________
    
    Buy = ttk.Frame(mainframe)
    Buy.grid(row = 0, column = 1)
    Buy.grid_columnconfigure((0,1), weight = 1)
    Buy.grid_rowconfigure(0, weight = 1)
    
    # Scrollbox
    
    listbox = Listbox(mainframe) 
    listbox.grid(row = 0, column = 0)
    
    
        
    
    # Labels 
    
    price_label = ttk.Label(Buy, text=f"Price")
    price_label.config(font=("Courier", 16))
    price_label.grid(column=0, row=0)
    
    feet_price = StringVar()
    entry_price = ttk.Entry(Buy, textvariable=feet_price)
    entry_price.grid(row=0, column=1, padx=20, pady=5)
    
    


    amount_label = ttk.Label(Buy, text=f"Amount")
    amount_label.grid(column=0, row=1)
    amount_label.config(font=("Courier", 16))
    
    feet_amount = StringVar()
    entry_amount = ttk.Entry(Buy, textvariable=feet_amount)
    entry_amount.grid(row=1, column=1, padx=20, pady=5)
    
    
    Button(Buy, text=f"Buy", command=lambda i=0: buy_func(feet_price, feet_amount),width=18, height=2,bg="red", fg="white").grid(column=1, row=2)
    
    
    # SELL__________________________
    
    Sell = ttk.Frame(mainframe)
    Sell.grid(row = 0, column = 2)
    Sell.grid_columnconfigure((0,1), weight = 1)
    Sell.grid_rowconfigure(0, weight = 1)
    
    # Scrollbox
    
    listbox = Listbox(mainframe) 
    listbox.grid(row = 0, column = 3)
    
    
    
    
    # Labels 
    
    price_label = ttk.Label(Sell, text=f"Price")
    price_label.config(font=("Courier", 16))
    price_label.grid(column=1, row=0)
    
    feet_price_sell = StringVar()
    entry_price = ttk.Entry(Sell, textvariable=feet_price_sell)
    entry_price.grid(row=0, column=2, padx=20, pady=5)
    
    


    amount_label = ttk.Label(Sell, text=f"Amount")
    amount_label.grid(column=1, row=1)
    amount_label.config(font=("Courier", 16))
    
    feet_amount_sell = StringVar()
    entry_amount = ttk.Entry(Sell, textvariable=feet_amount_sell)
    entry_amount.grid(row=1, column=2, padx=20, pady=5)
    
    
    Button(Sell, text=f"Sell", command=lambda i=0: sell_func(feet_price_sell, feet_amount_sell), width=18, height=2,bg="green", fg="white").grid(column=2, row=2)
    
    
    
     
    

    
    


    entry_price.focus()

    root.mainloop()
    
          
open_game_window()
            
#open_login_window()