import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ATTENDANCE_DIR = os.path.join(BASE_DIR, "attendance")
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
TRAINER_DIR = os.path.join(BASE_DIR, "trainer")
UNKNOWN_DIR = os.path.join(BASE_DIR, "unknown")


REPORTS_DIR = os.path.join(BASE_DIR, "reports")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data") 


EMP_CSV = os.path.join(DATA_DIR, "employees.csv")
USERS_CSV = os.path.join(DATA_DIR, "admins.csv")
TEAM_CSV = os.path.join(DATA_DIR, "managers.csv")


FRONTAL_DEFAULT_XML = os.path.join(MODELS_DIR, "haarcascade_frontalface_default.xml")
FRONTAL_ALT2_XML = os.path.join(MODELS_DIR, "haarcascade_frontalface_alt2.xml")
PROFILE_XML = os.path.join(MODELS_DIR, "haarcascade_profileface.xml")


FACE_SIZE = (200, 200)  

OFFICE_START_TIME = "09:30"  

FOLDERS = [
    ATTENDANCE_DIR,
    DATASET_DIR,
    TRAINER_DIR,
    UNKNOWN_DIR,
    REPORTS_DIR,
    LOGS_DIR,
    MODELS_DIR,
    DATA_DIR
]

for folder in FOLDERS:
    os.makedirs(folder, exist_ok=True)
