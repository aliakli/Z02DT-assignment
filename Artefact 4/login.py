import tkinter as tk
from tkinter import messagebox
from dbmanager import UserManagement, Logs

# Function to validate the login

class Login:
    def __init__(self):
    # Create the main window
        self.db = UserManagement()
        self.window = tk.Tk()

        
        self.window.geometry("300x300")
        self.window.title("Login Form")
        self.window.resizable(False,False)

        # Create and place the username label and entry
        username_label = tk.Label(self.window, text="Username:")
        username_label.pack()

        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        # Create and place the password label and entry
        password_label = tk.Label(self.window, text="Password:")
        password_label.pack()

        self.password_entry = tk.Entry(self.window, show="*")  # Show asterisks for password
        self.password_entry.pack()

        # Create and place the login button
        login_button = tk.Button(self.window, text="Login", command=self.validate_login)
        login_button.pack()

        # Start the Tkinter event loop
        self.window.mainloop()
        
    def validate_login(self):
        userid = self.username_entry.get()
        password = self.password_entry.get()

        # You can add your own validation logic here
        if not self.db.validate_user_login(userid, password):
            messagebox.showinfo("Invalid", "Invalid Login,\nTry again")
            Logs.log_change("Attempted to login", user = userid)
            return False
        else:
            messagebox.showinfo("Success", "Login Successful")
            Logs.log_change("Logged in", user = userid)
            self.window.destroy()
            return True

l = Login()
