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

# Global
balance = 0          # Hält das aktuelle Guthaben des Spielers 
user_id = 0          # Speichert die ID des aktuellen Benutzers 
random = 0           # Speichert eine zufällige Zahl "das letzte Ergebnis des Roulettrads"
table_id = 0         # Tisch-ID


delay_time = 5       # In Second





# LOGIN ------------------------------

def open_login_window():    #Erstellt ein Anmeldefenster, in dem der Benutzer seinen Namen eingeben und sich authentifizieren kann. 
    global login_window, entry_name, entry_url
    login_window = Tk()
    login_window.title("Auth")

    label_name = Label(login_window, text="Name:")
    label_name.grid(row=0, column=0, padx=20, pady=5)
    
    
    label_url = Label(login_window, text="URL:")
    label_url.grid(row=1, column=0, padx=20, pady=5)

    entry_name = Entry(login_window)
    entry_name.grid(row=0, column=1, padx=20, pady=5)
    
    entry_url = Entry(login_window)
    entry_url.grid(row=1, column=1, padx=20, pady=5)
    entry_url.insert(0, 'http://localhost:8000')

    button_register = Button(login_window, text="Auth", command=register_user)
    button_register.grid(row=2, column=1, pady=20)

    login_window.mainloop()



def check_user(name):
    try:
        r = requests.get(f"{url}/users/{name}")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException:
        return None     # Bei einem Fehler wird "None" zurückgegeben



def register_user():     # wird aufgerufen, wenn sich ein Benutzer angemeldet hat bzw. anmeldet
    global balance
    global user_id
    global url
    
    name = entry_name.get()
    if not name:         # Überprüft, ob der Name eingegeben wurde, und registriert den Benutzer über das Backend, wenn er noch nicht existiert.
        messagebox.showwarning("", "Wir sollen deinen Namen wissen, looser")
        return
    
    url_label = entry_url.get()
    
    url = url_label
    
    
    user_data = check_user(name)
    print(user_data)
    if user_data:
        # User exists
        user_id = user_data['id']
        balance = user_data['balance']
        login_window.destroy()
        open_table_window()
    else:
        try:
            r = requests.post(f"{url}/users/", json={'name': name})
            r.raise_for_status()
            print(r.json())
            messagebox.showinfo("", f"Willkommen, {name}, in the best Roulette in the world")
            
            # Daten for local
            balance = 100
            user_id = r.json()['id']
            
            login_window.destroy()
            open_table_window()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("", f"No Internet {e}")


# Tables

def open_table_window(): 
    global table_windows
    table_windows = Tk()
    table_windows.title("Choose Table")

    # Window settings
    gameframe = ttk.Frame(table_windows, padding="20 20 20 20")
    gameframe.grid(column=0, row=0)
    table_windows.columnconfigure(0, weight=1)
    table_windows.rowconfigure(0, weight=1)
    
    try:
        r = requests.get(f"{url}/tables")
        r.raise_for_status()
        tables_arr = r.json()['tables']
        column_index = 0
        
        for table in tables_arr:
            Button(gameframe, text=f"Table {table}", command=lambda table=table: choose_table(table)).grid(row=1, column=column_index)
            column_index += 1

    except requests.exceptions.RequestException as e:
        messagebox.showerror("", f"No Internet")
        
    table_windows.mainloop()



def choose_table(table):
    global table_id, table_windows
    table_id = table  
    
    table_windows.destroy()
    open_game_window() 
    
    
    
def update_tables():
    global table_id
    
    try:
        r = requests.get(f"{url}/tables")
        r.raise_for_status()
        tables_arr = r.json()['tables']
        for table in tables_arr:
            Button(table_windows, text=f"Table {table}", command=lambda table=table: choose_table(table)).grid(row=2, column=table+5, sticky=(S, E))
    except requests.exceptions.RequestException as e:
        messagebox.showerror("", f"No Internet")
    





# BETS ------------------------------

# Make a bet with a number  
def make_bet_digit(number, bet):  
    global balance, user_id, table_id
    
    type = "number"
    value = str(number)
    
    # Bet
    try:
        amount = int(bet.get())
    except:
        amount = 0
    if amount > balance: 
        messagebox.showwarning("", "Du hast kein Geld mehr\n\n Guthaben aufladen?\n\n Paypal: @perf007\n Text: nickname (Optional)")
    elif amount < 0:
        messagebox.showwarning("", "are u hacker?")
    elif amount == 0:
        messagebox.showwarning("", "ZERO?")
    else:
        try:
            r = requests.post(f"{url}/bet", json = {'user_id': str(user_id), "table_id": table_id - 1, "type": type, 'value': value, 'amount': amount})
            r.raise_for_status()
            
            # update balance local
            balance -= amount 
            update_balance_label()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("", f"No Internet")
            pass
        
        
    
def make_bet_col(value, bet):
    global balance, user_id, table_id
    
    type = "col"
    
    # Bet
    try:
        amount = int(bet.get())
    except:
        amount = 0
    if amount > balance: 
        messagebox.showwarning("", "Du hast kein Geld mehr\n\n Guthaben aufladen?\n\n Paypal: @perf007\n Text: nickname (Optional)")
    elif amount < 0:
        messagebox.showwarning("", "are u hacker?")
    elif amount == 0:
        messagebox.showwarning("", "ZERO?")
    else:
        try:
            r = requests.post(f"{url}/bet", json = {'user_id': str(user_id), "table_id": table_id - 1, "type": type, 'value': str(value), 'amount': amount})
            r.raise_for_status()
            
            # update balance local
            balance -= amount 
            update_balance_label()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("", f"No Internet")
            pass



def make_bet_dozen(value, bet):
    global balance, user_id, table_id
    
    type = "doz"
    
    # Bet
    try:
        amount = int(bet.get())
    except:
        amount = 0
    if amount > balance: 
        messagebox.showwarning("", "Du hast kein Geld mehr\n\n Guthaben aufladen?\n\n Paypal: @perf007\n Text: nickname (Optional)")
    elif amount < 0:
        messagebox.showwarning("", "are u hacker?")
    elif amount == 0:
        messagebox.showwarning("", "ZERO?")
    else:
        try:
            r = requests.post(f"{url}/bet", json = {'user_id': str(user_id), "table_id": table_id - 1, "type": type, 'value': str(value), 'amount': amount})
            r.raise_for_status()
            
            # update balance local
            balance -= amount 
            update_balance_label()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("", f"No Internet")
            pass
    
    
    
def make_bet_color(value, bet):
    global balance, user_id, table_id
    
    type = "color"
    
    # Bet
    try:
        amount = int(bet.get())
    except:
        amount = 0
    if amount > balance: 
        messagebox.showwarning("", "Du hast kein Geld mehr\n\n Guthaben aufladen?\n\n Paypal: @perf007\n Text: nickname (Optional)")
    elif amount < 0:
        messagebox.showwarning("", "are u hacker?")
    elif amount == 0:
        messagebox.showwarning("", "ZERO?")
    else:
        try:
            r = requests.post(f"{url}/bet", json = {'user_id': str(user_id), "table_id": table_id - 1, "type": type, 'value': str(value), 'amount': amount})
            r.raise_for_status()
            
            # update balance local
            balance -= amount 
            update_balance_label()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("", f"No Internet")
            pass  



def make_bet_parity(value, bet):
    global balance, user_id, table_id
    
    type = "parity"
    
    # Bet
    try:
        amount = int(bet.get())
    except:
        amount = 0
    if amount > balance: 
        messagebox.showwarning("", "Du hast kein Geld mehr\n\n Guthaben aufladen?\n\n Paypal: @perf007\n Text: nickname (Optional)")
    elif amount < 0:
        messagebox.showwarning("", "are u hacker?")
    elif amount == 0:
        messagebox.showwarning("", "ZERO?")
    else:
        try:
            r = requests.post(f"{url}/bet", json = {'user_id': str(user_id), "table_id": table_id - 1, "type": type, 'value': str(value), 'amount': amount})
            r.raise_for_status()
            
            # update balance local
            balance -= amount 
            update_balance_label()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("", f"No Internet")
            pass



    
    
    
    
# UPDATES  ------------------------------
def update_balance_label():
    balance_label.config(text=f"Balance: {str(balance)}")
    
def update_balance(server_balance):
    global balance
    balance += server_balance
    update_balance_label()
    
    
def update_random_label(random):
    if random < 10:
        random_label.config(text=f"{str(random)}", width=1)
    else:
        random_label.config(text=f"{str(random)}", width=2)
            
    
    
    
    
# GAME  ------------------------------
    
async def listen_for_updates():
    ws_url = url.replace('http', 'ws').replace('htpps', 'wss') + '/ws'
    print("Connecting")
    async with websockets.connect(ws_url) as websocket:
        print("Connected")
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                
                result = data['result']
                server_update = data['balance']
                win = data['win']
                user_from_server = data['user_id']
                
                if(user_from_server != user_id):
                    continue
                
                if 0 == win:
                    result_func(0)
                elif 1 == win:
                    result_func(1)
                
                update_random_label(int(result))
                update_balance(server_update)
                
            except websockets.ConnectionClosed:
                break


def start_websocket():
    def run_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(listen_for_updates())
    
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=run_loop, args=(loop,))
    t.start()


    
def update_gif(label, frames, ind):
    frame = frames[ind]
    ind += 1
    if ind == len(frames):
        ind = 0
    label.configure(image=frame)
    root.after(100, update_gif, label, frames, ind)
    
    
def clear_label(label):
    label.grid_forget()   
    
def result_func(res):
    
    gif_label = ttk.Label(frame_all_buttons)
    gif_label.grid(column=2, row=10)
    
    if res:
        gif_path = "../assets/data/fairoulette/win.gif"
        gif_image = Image.open(gif_path)
        frames = []
        try:
            while True:
                resized_frame = gif_image.copy().resize((600, 380)) 
                frames.append(ImageTk.PhotoImage(resized_frame))
                gif_image.seek(gif_image.tell() + 1) 
        except EOFError:
            pass
        update_gif(gif_label, frames, 0)
    else:
        loss_im = Image.open("../assets/data/fairoulette/loss.jpg").resize((600, 380))
        loss = ImageTk.PhotoImage(loss_im)
        gif_label.configure(image=loss)
        gif_label.image = loss
    root.after(delay_time * 1000, clear_label, gif_label)
    
        
    
    
    
    
def open_game_window():
    global root, balance_label, random, random_label, black, frame_all_buttons, loss, gif_label
    
    # Main window
    root = Tk()
    root.title("Fairoulette")

    # Window settings
    mainframe = ttk.Frame(root, padding="70 70 70 70")
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # ENTRYS 
    
    Entrys = ttk.Frame(mainframe)
    Entrys.grid(row = 1, column = 0)
    Entrys.grid_columnconfigure((0,1), weight = 1)
    Entrys.grid_rowconfigure(0, weight = 1)
    
    
    Wert_label = ttk.Label(mainframe, text=f"Wert:")
    Wert_label.grid(column=1, row=0, sticky=('NW'))
    Wert_label.config(font=("Courier", 20))
    
    feet = StringVar()
    feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
    feet_entry.grid(column=1, row=0, sticky=(''))
    feet_entry.config(font=("Courier", 20))
    
    
    # Images
               
    wheel_path = Image.open("../assets/data/fairoulette/wheel.png")
    wheel = ImageTk.PhotoImage(wheel_path) 
    loss_im = Image.open("../assets/data/fairoulette/wheel.png")
    loss = ImageTk.PhotoImage(loss_im) 
    
     
    # Labels 
     
    wheel_label = ttk.Label(Entrys, image=wheel)
    wheel_label.grid(column=0, row=5)
    
    random_label = ttk.Label(Entrys, text=f"-")
    random_label.config(font=("Courier", 64), width=1)
    random_label.grid(column=0, row=5)
    
    
    empty_label = ttk.Label(Entrys, text=f" ")
    empty_label.grid(column=0, row=6)
    empty_label.config(font=("Courier", 36))


    balance_label = ttk.Label(Entrys, text=f"Balance: {str(balance)}")
    balance_label.grid(column=0, row=7)
    balance_label.config(font=("Courier", 20))
    
    
    empty_label = ttk.Label(Entrys, text=f" ")
    empty_label.grid(column=0, row=8)
    empty_label.config(font=("Courier", 55))
    
    table_label = ttk.Label(Entrys, text=f"Table: {str(table_id)}")
    table_label.grid(column=0, row=9)
    table_label.config(font=("Courier", 12))
    
    empty_label = ttk.Label(Entrys, text=f"   ")
    empty_label.grid(column=0, row=10)
    empty_label.config(font=("Courier", 86))
    
    empty_label = ttk.Label(Entrys, text=f"   ")
    empty_label.grid(column=0, row=11)
    empty_label.config(font=("Courier", 36))





    # GAMEBOARD
    
    frame_all_buttons= ttk.Frame(mainframe)
    frame_all_buttons.grid(row = 1, column = 1, sticky=('N'))
    frame_all_buttons.grid_columnconfigure((0,1), weight = 1)
    frame_all_buttons.grid_rowconfigure(0, weight = 1)
    
    empty_label = ttk.Label(frame_all_buttons, text=f" ")
    empty_label.grid(column=0, row=0)
    empty_label.config(font=("Courier", 40))
    
    # Green
    frame_buttons = ttk.Frame(frame_all_buttons)
    frame_buttons.grid(row = 2, column = 1)
    frame_buttons.grid_columnconfigure((0,1), weight = 1)
    frame_buttons.grid_rowconfigure(0, weight = 1)
    
    Button(frame_buttons, text=f"{0}", command=lambda i=0: make_bet_digit(i, feet), width=4, height=7,bg="green", fg="white").grid(column=0, row=0)
    
    
    # Numbers
    
    frame_buttons = ttk.Frame(frame_all_buttons)
    frame_buttons.grid(row = 2, column = 2)
    frame_buttons.grid_columnconfigure((0,1), weight = 1)
    frame_buttons.grid_rowconfigure(0, weight = 1)
    
    black = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35]
    f_row = [3,6,9,12,15,18,21,24,27,30,33,36]
    s_row = [2,5,8,11,14,17,20,23,26,29,32,35]
    th_row = [1,4,7,10,13,16,19,22,25,28,31,34]
    
    rows = [f_row, s_row, th_row]
    row_numbers = 0
    column_numbers = 0
    
    for row in rows:
        for i in row:
                color = is_black(i)
                if column_numbers < 12:
                    Button(frame_buttons, text=f"{i}", command=lambda i=i: make_bet_digit(i, feet), width=4, height=2,bg=color, fg="white").grid(column=column_numbers, row=row_numbers)
                    column_numbers += 1
                else:
                    column_numbers = 0
                    Button(frame_buttons, text=f"{i}", command=lambda i=i: make_bet_digit(i, feet), width=4, height=2,bg=color, fg="white").grid(column=column_numbers, row=row_numbers)
                    column_numbers += 1
                    
        row_numbers = row_numbers + 1
    
    # Dozen
    
    frame_buttons = ttk.Frame(frame_all_buttons)
    frame_buttons.grid(row = 5, column = 2)
    frame_buttons.grid_columnconfigure((0,1), weight = 1)
    frame_buttons.grid_rowconfigure(0, weight = 1)
    
    
    Button(frame_buttons, text=f"1 st 12", command=lambda i=0: make_bet_dozen(i, feet), width=23, height=2,bg="darkblue", fg="white").grid(column=0, row=0)
    Button(frame_buttons, text=f"2 nd 12", command=lambda i=1: make_bet_dozen(i, feet), width=22, height=2,bg="darkblue", fg="white").grid(column=1, row=0)
    Button(frame_buttons, text=f"3 rd 12", command=lambda i=2: make_bet_dozen(i, feet), width=23, height=2,bg="darkblue", fg="white").grid(column=2, row=0)
    
    # Col
    
    frame_buttons = ttk.Frame(frame_all_buttons)
    frame_buttons.grid(row = 2, column = 14)
    frame_buttons.grid_columnconfigure((0,1), weight = 1)
    frame_buttons.grid_rowconfigure(0, weight = 1)
    
    
    Button(frame_buttons, text=f"2 to 1", command=lambda i=0: make_bet_col(i, feet), width=15, height=2,bg="darkblue", fg="white").grid(column=0, row=0)
    Button(frame_buttons, text=f"2 to 1", command=lambda i=1: make_bet_col(i, feet), width=15, height=2,bg="darkblue", fg="white").grid(column=0, row=1)
    Button(frame_buttons, text=f"2 to 1", command=lambda i=2: make_bet_col(i, feet), width=15, height=2,bg="darkblue", fg="white").grid(column=0, row=2)
    
    # Parity
    
    frame_buttons = ttk.Frame(frame_all_buttons)
    frame_buttons.grid(row = 6, column = 2)
    frame_buttons.grid_columnconfigure((0,1), weight = 1)
    frame_buttons.grid_rowconfigure(0, weight = 1)
    
    
    Button(frame_buttons, text=f"Even", command=lambda i=0: make_bet_parity(i, feet), width=15, height=2,bg="white", fg="black").grid(column=0, row=0)
    Label(frame_buttons, text="                                                                    ").grid(column=1, row=0)
    Button(frame_buttons, text=f"Odd", command=lambda i=1: make_bet_parity(i, feet), width=15, height=2,bg="white", fg="black").grid(column=2, row=0)
    
    
    # Color bet
    
    frame_buttons = ttk.Frame(frame_all_buttons)
    frame_buttons.grid(row = 1, column = 2)
    frame_buttons.grid_columnconfigure((0,1), weight = 1)
    frame_buttons.grid_rowconfigure(0, weight = 1)
    
    
    Button(frame_buttons, text=f"BLACK", command=lambda i=0: make_bet_color("black", feet), width=35, height=2,bg="black", fg="white").grid(column=0, row=0)
    Button(frame_buttons, text=f"RED", command=lambda i=1: make_bet_color("red", feet), width=35, height=2,bg="#8B0000", fg="white").grid(column=1, row=0)
    
    
    # Image
    

    feet_entry.focus()
    
    # Listening for (updates) Daten from Server
    start_websocket()

    root.mainloop()
    
    

def is_black(i):   
    if i in black:
        return 'black'
    else:
        return "#8B0000"
    
#open_game_window()
open_login_window()

#open_table_window()