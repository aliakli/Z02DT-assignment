# ================= IMPORTS =================
from bidmas import Calculator  # Calculator logic
from login import Login  # Login system
from dbmanager import UserManagement  # Database manager
from test_calculator import TestCalculator  # Admin testing
from setup import Setup  # Database setup
import csv  # CSV export / search
import tkinter as tk  # GUI


# ================= LOG HANDLER =================
class CalcLogs:

    def __init__(self):
        self.UM = UserManagement("users")  # Connect to user database

    def add_to_db(self, user, expression, mode, error=None):
        self.UM.add_calculation_logs(
            user, expression, mode, errors=error
        )

    def export(self):
        with open("calculation_logs.csv", "w", newline="") as file:
            calculations = self.UM.get_calculation_logs()
            writer = csv.writer(file)
            writer.writerow(
                ["UserID", "Expression", "Mode", "Errors", "Timestamp"]
            )
            writer.writerows(calculations)


# ================= MAIN CALCULATOR APP =================
class CalculatorApp:

    def __init__(self, root, user, isAdmin):
        self.UM = UserManagement("users")
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("650x500")

        self.instance = Calculator()
        self.logs = CalcLogs()
        self.user = user
        self.userid = None
        self.isAdmin = isAdmin
        self.userid = self.UM.get_userid(user)
        self.mode = "Radians"
        self.instance.angle_mode = True

        # Mode Label
        self.mode_label = tk.Label(
            root,
            text=f"Mode: {self.mode}",
            font=("Arial", 12),
        )
        self.mode_label.pack(pady=5)

        # -------- Output Frame --------
        output_frame = tk.Frame(root)
        output_frame.pack(pady=10)

        self.scrollbar = tk.Scrollbar(output_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output = tk.Text(
            output_frame,
            height=15,
            width=75,
            state="disabled",
            yscrollcommand=self.scrollbar.set,
        )
        self.output.pack(side=tk.LEFT)

        self.scrollbar.config(command=self.output.yview)

        # -------- Input Field --------
        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.process_expression)

        # -------- Buttons --------
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Calculate",
            command=self.process_expression,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Switch Mode",
            command=self.toggle_mode,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Clear Screen",
            command=self.clear_screen,
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="View My History",
            command=self.view_user_history,
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            button_frame,
            text="Exit",
            command=self.exit_program,
        ).grid(row=0, column=4, padx=5)

    # Write to output
    def write_output(self, text):
        self.output.config(state="normal")
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state="disabled")

    # Toggle Degrees/Radians
    def toggle_mode(self):
        self.instance.angle_mode = not self.instance.angle_mode
        self.mode = (
            "Radians" if self.instance.angle_mode else "Degrees"
        )
        self.mode_label.config(text=f"Mode: {self.mode}")
        self.write_output(f"Switched to {self.mode}\n")

    # Clear output display
    def clear_screen(self):
        self.output.config(state="normal")
        self.output.delete(1.0, tk.END)
        self.output.config(state="disabled")

    # Search CSV for the user's history
    def view_user_history(self):
        try:
            with open("calculation_logs.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)

                found = False
                self.write_output(
                    "\n--- Your Calculation History ---\n"
                )

                for row in reader:
                    userid, expression, mode, errors, timestamp = row

                    if int(userid) == self.userid:
                        found = True
                        if errors:
                            self.write_output(
                                f"{expression} | {mode} | "
                                f"ERROR: {errors} | {timestamp}\n"
                            )
                        else:
                            self.write_output(
                                f"{expression} | {mode} | "
                                f"{timestamp}\n"
                            )

                if not found:
                    self.write_output(
                        "No history found for this user.\n"
                    )

                self.write_output(
                    "--- End of History ---\n\n"
                )

        except FileNotFoundError:
            self.write_output(
                "No log file found. Please exit once to generate it.\n"
            )

    # -------- Process expression --------
    def process_expression(self, event=None):
        expression = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if expression == "":
            return

        if expression == "test" and self.isAdmin:
            test = TestCalculator()
            test.test_calculator()
            self.write_output("Admin tests executed.\n")
            return

        try:
            result = self.instance.tokenise_expression(
                expression.replace("^", "**")
            )
            self.write_output(f"{expression} = {result}\n")
            self.logs.add_to_db(
                self.user,
                f"{expression}={result}",
                self.mode,
            )

        except Exception as err:
            if len(expression) > 0 and not expression[0].isdigit():
                self.write_output("Invalid syntax\n")
                self.logs.add_to_db(
                    self.user,
                    expression,
                    self.mode,
                    error="Syntax Error",
                )
            else:
                self.write_output(f"Error: {str(err)}\n")
                self.logs.add_to_db(
                    self.user,
                    expression,
                    self.mode,
                    error=str(err),
                )

    # Exit
    def exit_program(self):
        self.logs.export()
        self.root.destroy()


# ================= MAIN FUNCTION =================
def main():
    db = Setup()
    db.setup()

    login = Login()

    if not login.isLoggedIn:
        return

    root = tk.Tk()
    app = CalculatorApp(root, login.user, login.isAdmin)
    root.mainloop()


# Prevent running when imported
if __name__ == "__main__":
    main()
