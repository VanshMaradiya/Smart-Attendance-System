import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os


def run_script(script_name: str, extra_args=None):
    """
    Run python scripts safely from GUI with extra command arguments.
    """
    try:
        script_path = os.path.join(os.path.dirname(__file__), script_name)

        if not os.path.exists(script_path):
            messagebox.showerror("Error", f"File not found:\n{script_path}")
            return

        cmd = [sys.executable, script_path]

        if extra_args:
            cmd.extend(extra_args)

        subprocess.Popen(cmd)

    except Exception as e:
        messagebox.showerror("Error", str(e))


class RoleDashboard:
    def __init__(self, root, user_info: dict):
        self.root = root
        self.user_info = user_info

        role = user_info["role"]
        name = user_info["name"]

        self.root.title(f"Dashboard - {role.upper()} - {name}")
        self.root.geometry("520x520")
        self.root.resizable(False, False)

        title = tk.Label(root, text="Smart Attendance System", font=("Arial", 18, "bold"))
        title.pack(pady=15)

        tk.Label(root, text=f"Welcome: {name}", font=("Arial", 12)).pack()
        tk.Label(root, text=f"Role: {role.upper()}", font=("Arial", 12, "bold")).pack(pady=5)

        frame = tk.Frame(root)
        frame.pack(pady=25)

        btn_style = {"font": ("Arial", 12), "width": 28, "height": 2}

        # ✅ ADMIN DASHBOARD
        if role == "admin":
            tk.Button(frame, text="1) Register Face", command=lambda: run_script("register_face.py"), **btn_style).pack(pady=8)
            tk.Button(frame, text="2) Train Model", command=lambda: run_script("train_model.py"), **btn_style).pack(pady=8)
            tk.Button(frame, text="3) Mark Attendance", command=lambda: run_script("mark_attendance.py"), **btn_style).pack(pady=8)
            tk.Button(frame, text="4) Attendance Report", command=lambda: run_script("attendance_report_gui.py"), **btn_style).pack(pady=8)

        # ✅ MANAGER DASHBOARD
        elif role == "manager":
            tk.Button(
                frame,
                text="View Team Attendance Report",
                command=lambda: run_script("attendance_report_gui.py"),
                **btn_style
            ).pack(pady=8)

            tk.Label(frame, text="(Team filter can be added next)", font=("Arial", 10)).pack(pady=2)

        # ✅ EMPLOYEE DASHBOARD
        elif role == "employee":
            tk.Button(
                frame,
                text="View My Attendance Report",
                command=lambda: run_script("attendance_report_gui.py"),
                **btn_style
            ).pack(pady=8)

            tk.Label(frame, text="(Self filter can be added next)", font=("Arial", 10)).pack(pady=2)

        else:
            tk.Label(frame, text="Unknown role found!", fg="red").pack(pady=10)

        tk.Button(root, text="Logout", command=self.logout, **btn_style).pack(pady=30)

    def logout(self):
        self.root.destroy()
        run_script("login.py")
