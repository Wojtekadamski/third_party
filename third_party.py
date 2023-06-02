import requests
import tkinter as tk
from tkinter import messagebox

API_URL = 'http://localhost:5000/api'  # Replace with your API's URL
API_KEY = 'api_key_1'  # Replace with your API key
API_SECRET = 'secret_1'  # Replace with your API secret

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("300x300")
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(3, weight=1)

        self.username_label = tk.Label(self, text="Username")
        self.username_label.grid(row=1, column=1)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=2)

        self.password_label = tk.Label(self, text="Password")
        self.password_label.grid(row=2, column=1)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=2)

        self.submit_button = tk.Button(self, text="Submit", command=self.initiate_s2fa)
        self.submit_button.grid(row=3, column=1, columnspan=2)

        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.grid(row=4, column=1, columnspan=2)

    def initiate_s2fa(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            response = requests.post(
                f'{API_URL}/s2fa/initiate',
                headers={'Authorization': f'Bearer {API_KEY}', 'X-API-Secret': API_SECRET},
                json={'username': username, 'password': password}
            )
            if response.status_code == 200:
                self.s2fa_code = response.json().get('s2fa_code')
                self.create_2fa_widgets()
            else:
                self.error_label['text'] = 'Error: Invalid username or password'
        except requests.exceptions.RequestException as e:
            self.error_label['text'] = 'Error: Could not connect to the server'

    def create_2fa_widgets(self):
        self.code_label = tk.Label(self, text="2FA Code")
        self.code_label.grid(row=4, column=0)
        self.code_entry = tk.Entry(self)
        self.code_entry.grid(row=4, column=1)

        self.verify_button = tk.Button(self, text="Verify", command=self.verify_s2fa)
        self.verify_button.grid(row=5, column=0, columnspan=2)

    def verify_s2fa(self):
        token = self.code_entry.get()
        try:
            response = requests.post(
                f'{API_URL}/s2fa/verify',
                headers={'Authorization': f'Bearer {API_KEY}', 'X-API-Secret': API_SECRET},
                json={'username': self.username_entry.get(), 'token': token}
            )
            if response.status_code == 200 and response.json().get('result') == 'success':
                messagebox.showinfo("Success", "You are logged in!")
            else:
                self.error_label['text'] = 'Error: Invalid 2FA code'
        except requests.exceptions.RequestException as e:
            self.error_label['text'] = 'Error: Could not connect to the server'

root = tk.Tk()
app = Application(master=root)
app.mainloop()

