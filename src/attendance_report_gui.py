import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

from config import ATTENDANCE_DIR, REPORTS_DIR


# Helper: get file path by date
def attendance_file_by_date(date_str: str):
    file_path = os.path.join(ATTENDANCE_DIR, f"{date_str}.csv")
    if os.path.exists(file_path):
        return file_path
    return None


# Helper: get latest file
def latest_attendance_file():
    if not os.path.exists(ATTENDANCE_DIR):
        return None

    files = [f for f in os.listdir(ATTENDANCE_DIR) if f.endswith(".csv")]
    if not files:
        return None

    files.sort(reverse=True)
    return os.path.join(ATTENDANCE_DIR, files[0])


# Read attendance range
def read_attendance_range(from_date: str, to_date: str):
    start = datetime.strptime(from_date, "%Y-%m-%d")
    end = datetime.strptime(to_date, "%Y-%m-%d")

    if start > end:
        raise ValueError("From date cannot be greater than To date")

    all_data = []
    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        fp = attendance_file_by_date(date_str)
        if fp:
            df = pd.read_csv(fp)
            df["File"] = os.path.basename(fp)  # optional
            all_data.append(df)

        current += pd.Timedelta(days=1)

    if not all_data:
        return None

    return pd.concat(all_data, ignore_index=True)


# PDF Export (ReportLab)
def export_pdf(df: pd.DataFrame, file_path: str):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError:
        raise ImportError(
            "reportlab not installed. Install using: pip install reportlab")

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Attendance Report")

    c.setFont("Helvetica", 10)
    y = height - 80

    # column headers
    cols = list(df.columns)
    line = " | ".join(cols)
    c.drawString(50, y, line)
    y -= 20

    c.setFont("Helvetica", 9)
    for _, row in df.iterrows():
        values = [str(row[col]) for col in cols]
        line = " | ".join(values)

        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 9)
            y = height - 50

        c.drawString(50, y, line[:120])  # cut long line
        y -= 15

    c.save()


class AttendanceReportGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Report")
        self.root.geometry("1000x600")

        self.df = None

        # Filters Frame
        filter_frame = tk.Frame(root)
        filter_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(filter_frame, text="Mode:").grid(row=0, column=0, padx=5)
        self.mode_var = tk.StringVar(value="latest")
        self.mode_dropdown = ttk.Combobox(filter_frame,
                                          textvariable=self.mode_var,
                                          values=["latest", "date", "range"],
                                          state="readonly",
                                          width=15)
        self.mode_dropdown.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Date (YYYY-MM-DD):").grid(row=0,
                                                               column=2,
                                                               padx=5)
        self.date_entry = tk.Entry(filter_frame, width=15)
        self.date_entry.grid(row=0, column=3, padx=5)

        tk.Label(filter_frame, text="From:").grid(row=0, column=4, padx=5)
        self.from_entry = tk.Entry(filter_frame, width=15)
        self.from_entry.grid(row=0, column=5, padx=5)

        tk.Label(filter_frame, text="To:").grid(row=0, column=6, padx=5)
        self.to_entry = tk.Entry(filter_frame, width=15)
        self.to_entry.grid(row=0, column=7, padx=5)

        tk.Button(filter_frame, text="Load Report",
                  command=self.load_report).grid(row=0, column=8, padx=10)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(btn_frame, text="Export Excel",
                  command=self.export_excel).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Export PDF",
                  command=self.export_pdf_report).pack(side="left", padx=5)

        # Table Frame
        table_frame = tk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame,
                                  orient="vertical",
                                  command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def load_report(self):
        mode = self.mode_var.get()

        try:
            if mode == "latest":
                fp = latest_attendance_file()
                if not fp:
                    messagebox.showerror("Error", "No attendance file found!")
                    return
                self.df = pd.read_csv(fp)

            elif mode == "date":
                date_str = self.date_entry.get().strip()
                if not date_str:
                    messagebox.showerror("Error", "Please enter date!")
                    return

                fp = attendance_file_by_date(date_str)
                if not fp:
                    messagebox.showerror(
                        "Error", f"No file found for date: {date_str}")
                    return
                self.df = pd.read_csv(fp)

            elif mode == "range":
                from_date = self.from_entry.get().strip()
                to_date = self.to_entry.get().strip()
                if not from_date or not to_date:
                    messagebox.showerror("Error",
                                         "Please enter from and to dates!")
                    return

                df = read_attendance_range(from_date, to_date)
                if df is None:
                    messagebox.showerror(
                        "Error",
                        "No attendance files found in this date range!")
                    return
                self.df = df

            self.show_table()
            messagebox.showinfo("Success", "Report loaded successfully ")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_table(self):
        # clear existing table
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
        self.tree.delete(*self.tree.get_children())

        if self.df is None or self.df.empty:
            return

        cols = list(self.df.columns)
        self.tree["columns"] = cols

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row.values))

    def export_excel(self):
        if self.df is None or self.df.empty:
            messagebox.showerror("Error", "No data to export!")
            return

        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_path = os.path.join(REPORTS_DIR,
                                    f"attendance_report_{ts}.xlsx")

        file_path = filedialog.asksaveasfilename(
            initialfile=os.path.basename(default_path),
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")])

        if not file_path:
            return

        self.df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", f"Excel exported \n{file_path}")

    def export_pdf_report(self):
        if self.df is None or self.df.empty:
            messagebox.showerror("Error", "No data to export!")
            return

        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_path = os.path.join(REPORTS_DIR, f"attendance_report_{ts}.pdf")

        file_path = filedialog.asksaveasfilename(
            initialfile=os.path.basename(default_path),
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")])

        if not file_path:
            return

        try:
            export_pdf(self.df, file_path)
            messagebox.showinfo("Success", f"PDF exported \n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = AttendanceReportGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
