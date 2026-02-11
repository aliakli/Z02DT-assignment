import tkinter as tk
from tkinter import messagebox
from dbmanager import UserManagement, Logs

# Function to validate the login

class Login:
    def __init__(self):
        self.isAdmin = False
        self.isLoggedIn = False
        self.user = ""
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
        
        register_button = tk.Button(self.window, text="Register", command = self.register_user)
        register_button.pack()
        # Start the Tkinter event loop
        self.window.mainloop()
        
    def validate_login(self):
        userid = self.username_entry.get()
        password = self.password_entry.get()
        
        if not self.db.validate_user_login(userid, password):
            messagebox.showinfo("Invalid", "Invalid Login,\nTry again")
            Logs.log_change("Attempted to login", user = userid)
            return False
        else:
            messagebox.showinfo("Success", "Login Successful")
            Logs.log_change("Logged in", user = userid)
            self.isLoggedIn = True
            self.user += userid
            self.window.destroy()
            if userid == "admin":
                self.isAdmin = True
            return True
        
        
    def register_user(self):
        self.window.destroy()
        Register()
        
class Register:
    def __init__(self):
        self.db = UserManagement()
        self.window = tk.Tk()

        self.window.geometry("300x300")
        self.window.title("Register")
        self.window.resizable(False, False)

        # Username
        tk.Label(self.window, text="New Username:").pack()
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        # Password
        tk.Label(self.window, text="New Password:").pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        # Confirm Password
        tk.Label(self.window, text="Confirm Password:").pack()
        self.confirm_entry = tk.Entry(self.window, show="*")
        self.confirm_entry.pack()

        # Register Button
        tk.Button(
            self.window,
            text="Create Account",
            command=self.create_account
        ).pack(pady=10)

        self.window.mainloop()

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            self.db.create_user(username, password)
            messagebox.showinfo("Success", "Account created successfully!")
            self.window.destroy()
            Login()

        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        
if __name__ == "__main__":            
    Login()
        


