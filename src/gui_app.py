import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os


def run_script(script_name: str):
    """
    Run python scripts safely from GUI.
    Example: run_script("register_face.py")
    """
    try:
        # ✅ Always run inside src folder
        script_path = os.path.join(os.path.dirname(__file__), script_name)

        if not os.path.exists(script_path):
            messagebox.showerror("Error", f"File not found:\n{script_path}")
            return

        # Run script with same python interpreter
        subprocess.Popen([sys.executable, script_path])

    except Exception as e:
        messagebox.showerror("Error", str(e))


class SmartAttendanceGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Smart Attendance System - Dashboard")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        # ✅ Title
        title = tk.Label(root,
                         text="Smart Attendance System",
                         font=("Arial", 20, "bold"))
        title.pack(pady=20)

        subtitle = tk.Label(root, text="Admin Dashboard", font=("Arial", 12))
        subtitle.pack(pady=5)

        # ✅ Buttons Frame
        frame = tk.Frame(root)
        frame.pack(pady=20)

        btn_style = {"font": ("Arial", 12), "width": 25, "height": 2}

        # ✅ Register Face
        tk.Button(frame,
                  text="1) Register Face",
                  command=lambda: run_script("register_face.py"),
                  **btn_style).pack(pady=8)

        # ✅ Train Model
        tk.Button(frame,
                  text="2) Train Model",
                  command=lambda: run_script("train_model.py"),
                  **btn_style).pack(pady=8)

        # ✅ Mark Attendance
        tk.Button(frame,
                  text="3) Mark Attendance",
                  command=lambda: run_script("mark_attendance.py"),
                  **btn_style).pack(pady=8)

        # ✅ Attendance Report GUI
        tk.Button(frame,
                  text="4) Attendance Report",
                  command=lambda: run_script("attendance_report_gui.py"),
                  **btn_style).pack(pady=8)

        # ✅ Exit
        tk.Button(frame,
                  text="Exit",
                  command=self.root.quit,
                  font=("Arial", 12),
                  width=25,
                  height=2).pack(pady=20)


def main():
    root = tk.Tk()
    app = SmartAttendanceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
