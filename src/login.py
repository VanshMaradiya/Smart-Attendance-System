import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from auth import authenticate, register_user
from role_dashboard import RoleDashboard

class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Smart Attendance System")
        self.root.geometry("450x420")
        self.root.resizable(False, False)

        tk.Label(root, text="Smart Attendance System", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(root, text="Login", font=("Arial", 14)).pack(pady=5)

        frame = tk.Frame(root)
        frame.pack(pady=15)

        # username
        tk.Label(frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = tk.Entry(frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # password
        tk.Label(frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # role dropdown
        tk.Label(frame, text="Role:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.role_var = tk.StringVar(value="admin")
        self.role_dropdown = ttk.Combobox(
            frame,
            textvariable=self.role_var,
            values=["admin", "manager", "employee"],
            state="readonly",
            width=18
        )
        self.role_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Login", font=("Arial", 12), width=14, command=self.login).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Register", font=("Arial", 12), width=14, command=self.open_register).grid(row=0, column=1, padx=10)

        tk.Button(root, text="Exit", font=("Arial", 12), width=32, command=root.quit).pack(pady=10)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get().strip()

        if not username or not password or not role:
            messagebox.showerror("Error", "Please enter username, password and role!")
            return

        user_info = authenticate(username, password, role)

        if not user_info:
            messagebox.showerror("Login Failed", "Invalid username/password/role ❌")
            return

        messagebox.showinfo("Success", f"Welcome {user_info['name']} ✅")

        # open dashboard
        self.root.destroy()
        dashboard_root = tk.Tk()
        RoleDashboard(dashboard_root, user_info)
        dashboard_root.mainloop()

    def open_register(self):
        RegisterWindow(self.root)


class RegisterWindow:
    def __init__(self, parent_root):
        self.window = tk.Toplevel(parent_root)
        self.window.title("Register New User")
        self.window.geometry("450x420")
        self.window.resizable(False, False)

        tk.Label(self.window, text="Register User", font=("Arial", 16, "bold")).pack(pady=20)

        frame = tk.Frame(self.window)
        frame.pack(pady=10)

        # name
        tk.Label(frame, text="Full Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = tk.Entry(frame, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        # username
        tk.Label(frame, text="Username:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = tk.Entry(frame, font=("Arial", 12))
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        # password
        tk.Label(frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        # role
        tk.Label(frame, text="Role:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.role_var = tk.StringVar(value="employee")
        self.role_dropdown = ttk.Combobox(
            frame,
            textvariable=self.role_var,
            values=["admin", "manager", "employee"],
            state="readonly",
            width=18
        )
        self.role_dropdown.grid(row=3, column=1, padx=10, pady=10)

        # buttons
        tk.Button(self.window, text="Create Account", font=("Arial", 12), width=25, command=self.register).pack(pady=20)
        tk.Button(self.window, text="Close", font=("Arial", 12), width=25, command=self.window.destroy).pack()

    def register(self):
        name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get().strip()

        if not name or not username or not password or not role:
            messagebox.showerror("Error", "All fields are required!")
            return

        ok, msg = register_user(username, password, role, name)

        if ok:
            messagebox.showinfo("Success", msg)
            # ✅ redirect to login (close register window)
            self.window.destroy()
        else:
            messagebox.showerror("Error", msg)


def main():
    root = tk.Tk()
    LoginGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
