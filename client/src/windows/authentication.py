from tkinter import Tk, Label, Entry, Button, messagebox

import jwt
import requests

from interactions.authentication import server_auth_user
from state import WindowState


class AuthenticationWindow(Tk):
    entry_name: Entry
    entry_pasword: Entry
    entry_url: Entry

    def __init__(self, state: WindowState):
        super().__init__()
        self.state = state
        self.open_login_window()

    def open_login_window(self):

        self.title("Auth")

        # Email
        label_name = Label(self, text="E-Mail:")
        label_name.grid(row=0, column=0, padx=20, pady=5)

        self.entry_name = Entry(self)
        self.entry_name.grid(row=0, column=1, padx=20, pady=5)

        # Pass
        label_password = Label(self, text="Pass:")
        label_password.grid(row=1, column=0, padx=20, pady=5)

        self.entry_pasword = Entry(self, show="*")
        self.entry_pasword.grid(row=1, column=1, padx=20, pady=5)

        # URL
        self.label_url = Label(self, text="URL:")
        self.label_url.grid(row=2, column=0, padx=20, pady=5)

        self.entry_url = Entry(self)
        self.entry_url.grid(row=2, column=1, padx=20, pady=5)
        self.entry_url.insert(0, 'http://localhost:8000')

        # Buttons
        button_reg = Button(self, text="Reg", command=self.register_user)
        button_reg.grid(row=3, column=0, pady=20)

        button_login = Button(self, text="Login", command=self.login)
        button_login.grid(row=3, column=1, pady=20)

    def login(self):
        email = self.entry_name.get()
        password = self.entry_pasword.get()

        if not email:
            messagebox.showwarning("", "Name is required")
            return

        if not password:
            messagebox.showwarning("", "Password is required")
            return

        url = self.entry_url.get()
        self.state.url = url

        token, user_data = server_auth_user(self.state.url, email, password)

        if token != '':
            # Wellcome func HERE
            messagebox.showinfo("", f"Welcome")

            self.state.user_id = jwt.decode(token, self.state.SECRET_KEY, algorithms=["HS256"])["user_id"]
            self.state.user_email = jwt.decode(token, self.state.SECRET_KEY, algorithms=["HS256"])["sub"]
            # get_user_balance(user_email)
            self.state.token = token

            self.destroy()

        elif user_data == "Incorrect email or password":
            messagebox.showinfo("", f"{user_data}")
        elif user_data == "user in nor register":
            messagebox.showinfo("", f"You need to register")
        else:
            messagebox.showinfo("", f"No Internet!")

    def register_user(self):

        email = self.entry_name.get()
        password = self.entry_pasword.get()

        if not email:
            messagebox.showwarning("", "Email is required")
            return

        if not password:
            messagebox.showwarning("", "Password is required")
            return

        url_label = self.entry_url.get()
        url = url_label

        try:
            data = {'email': email, 'password': password}
            r = requests.post(f"{url}/register", json=data)
            r.raise_for_status()
            if r.json()['status'] == 'reg complete':
                token, user_data = server_auth_user(self.state.url, email, password)

                # Wellcome func HERE
                messagebox.showinfo("", f"Welcome")

                self.state.user_id = jwt.decode(token, self.state.SECRET_KEY, algorithms=["HS256"])["user_id"]
                self.state.user_email = jwt.decode(token, self.state.SECRET_KEY, algorithms=["HS256"])["sub"]
                # get_user_balance(user_email)
                self.state.token = token

                self.destroy()

                return r.json()
            else:
                messagebox.showinfo("", f"User already exists")
        except requests.exceptions.RequestException as e:
            messagebox.showinfo("", f"No Internet!")
            return None
