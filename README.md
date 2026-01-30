# 🧠 Smart Attendance System (Face Recognition)

A Python-based Smart Attendance System using OpenCV for face recognition and Tkinter for GUI.  
The system supports Admin, Manager and Employee roles, CSV-based user management, real-time attendance, reporting, and logging.

- opencv-python → camera + image processing
- opencv-contrib-python → LBPH face recognizer
- pandas → CSV handling + reports
- numpy → array operations (training)
- reportlab → PDF export
- Pillow → image handling (GUI / saving)

---

## ✨ Features

### 🔐 Authentication (CSV)
- Admin / Employee login
- User registration (username, password, role, name)
- Users stored in `data/users.csv`

### 📸 Face Registration
- Webcam-based face capture
- Automatic dataset creation per employee
- Saves cropped, resized faces for better accuracy

### ⏱ Attendance
- Real-time recognition
- One attendance per person per day
- On-Time / Late status
- Unknown person snapshot saving

### 📊 Reports
- View latest / specific date / date range attendance
- Export to Excel and PDF 

### 🖥 GUI Dashboard (Tkinter)
- Login screen

- Admin:
  - Register Face
  - Train Model
  - Mark Attendance
  - Attendance Report

- Manager:
  - View Self Attendance

- Employee:
  - View Self Attendance
- Logout






