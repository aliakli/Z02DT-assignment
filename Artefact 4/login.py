import tkinter as tk  # For GUI
from tkinter import messagebox  # For pop-up messages
from dbmanager import UserManagement, Logs  # For user database and logging

# Class to handle user login
class Login:
    def __init__(self):
        self.isAdmin = False  # Flag for admin user
        self.isLoggedIn = False  # Flag for login status
        self.user = ""  # Store current username
        
        # Initialize database and main window
        self.db = UserManagement()
        self.window = tk.Tk()
        self.window.geometry("300x300")
        self.window.title("Login Form")
        self.window.resizable(False, False)

        # Username label and entry
        username_label = tk.Label(self.window, text="Username:")
        username_label.pack()
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        # Password label and entry
        password_label = tk.Label(self.window, text="Password:")
        password_label.pack()
        self.password_entry = tk.Entry(self.window, show="*")  # Mask password input
        self.password_entry.pack()

        # Login button
        login_button = tk.Button(self.window, text="Login", command=self.validate_login)
        login_button.pack()
        
        # Register button
        register_button = tk.Button(self.window, text="Register", command=self.register_user)
        register_button.pack()
        
        # Start GUI loop
        self.window.mainloop()
        
    def validate_login(self):
        userid = self.username_entry.get()  # Get username input
        password = self.password_entry.get()  # Get password input
        
        if not self.db.validate_user_login(userid, password):  # Check credentials
            messagebox.showinfo("Invalid", "Invalid Login,\nTry again")
            Logs.log_change("Attempted to login", user=userid)  # Log failed attempt
            return False
        else:
            messagebox.showinfo("Success", "Login Successful")  # Show success
            Logs.log_change("Logged in", user=userid)  # Log successful login
            self.isLoggedIn = True
            self.user += userid  # Store logged-in user
            self.window.destroy()  # Close login window
            if userid == "admin" or userid == "test":
                self.isAdmin = True  # Grant admin privileges
            return True
        
    def register_user(self):
        self.window.destroy()  # Close login window
        Register()  # Open registration window
        
# Class to handle user registration
class Register:
    def __init__(self):
        self.db = UserManagement()  # Initialize database
        self.window = tk.Tk()
        self.window.geometry("300x300")
        self.window.title("Register")
        self.window.resizable(False, False)

        # New username
        tk.Label(self.window, text="New Username:").pack()
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        # New password
        tk.Label(self.window, text="New Password:").pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        # Confirm password
        tk.Label(self.window, text="Confirm Password:").pack()
        self.confirm_entry = tk.Entry(self.window, show="*")
        self.confirm_entry.pack()

        # Create account button
        tk.Button(
            self.window,
            text="Create Account",
            command=self.create_account
        ).pack(pady=10)

        self.window.mainloop()  # Start GUI loop

    def create_account(self):
        username = self.username_entry.get()  # Get username input
        password = self.password_entry.get()  # Get password input
        confirm = self.confirm_entry.get()  # Get confirmation input

        if not username or not password:  # Ensure fields are filled
            messagebox.showerror("Error", "All fields are required")
            return

        if password != confirm:  # Check password match
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            self.db.create_user(username, password)  # Add user to database
            messagebox.showinfo("Success", "Account created successfully!")  # Show success
            self.window.destroy()  # Close registration window
            Login()  # Return to login window

        except Exception as err:
            messagebox.showerror("Error", str(err))  # Show error if creation fails
        
# Start login GUI when script is run
if __name__ == "__main__":            
    Login()
