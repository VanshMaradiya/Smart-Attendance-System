import os
import pandas as pd
from config import DATA_DIR

#  CSV FILES FOR DIFFERENT ROLES

ADMINS_CSV = os.path.join(DATA_DIR, "admins.csv")
MANAGERS_CSV = os.path.join(DATA_DIR, "managers.csv")
EMPLOYEES_CSV = os.path.join(DATA_DIR, "employees.csv")


#  Get correct file path based on role
def _get_file_by_role(role: str):
    role = str(role).lower().strip()

    if role == "admin":
        return ADMINS_CSV
    elif role == "manager":
        return MANAGERS_CSV
    elif role == "employee":
        return EMPLOYEES_CSV

    return None


#  Create CSV file if not exists
def _ensure_file(file_path: str):
    # create /data folder if missing
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # create file with header if missing
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["username", "password", "name"])
        df.to_csv(file_path, index=False)


#  Authenticate (Login)
def authenticate(username: str, password: str, role: str):
    """
    Returns:
        dict user if login success
        None if login fail
    """
    file_path = _get_file_by_role(role)
    if not file_path:
        print("❌ Invalid role selected!")
        return None

    _ensure_file(file_path)

    # load csv
    df = pd.read_csv(file_path)

    # fix column names
    df.columns = [c.strip().lower() for c in df.columns]

    # safe check
    if not {"username", "password", "name"}.issubset(set(df.columns)):
        print("❌ CSV columns missing!")
        return None

    # clean csv values
    df["username"] = df["username"].astype(str).str.strip()
    df["password"] = df["password"].astype(str).str.strip()
    df["name"] = df["name"].astype(str).str.strip()

    # clean input
    username = str(username).strip()
    password = str(password).strip()
    role = str(role).strip().lower()

    # match user
    user = df[(df["username"] == username) & (df["password"] == password)]

    if user.empty:
        return None

    row = user.iloc[0]

    return {"username": row["username"], "role": role, "name": row["name"]}


#  Register User


def register_user(username: str, password: str, role: str, name: str):
    """
    Returns:
        (True, success_message)
        (False, error_message)
    """
    file_path = _get_file_by_role(role)
    if not file_path:
        return False, "❌ Invalid role selected!"

    _ensure_file(file_path)

    # load csv
    df = pd.read_csv(file_path)
    df.columns = [c.strip().lower() for c in df.columns]

    # clean input
    username = str(username).strip()
    password = str(password).strip()
    name = str(name).strip()
    role = str(role).strip().lower()

    # validation
    if username == "" or password == "" or name == "":
        return False, "❌ All fields required!"

    # username check
    if not df.empty:
        df["username"] = df["username"].astype(str).str.strip()

        if username in df["username"].values:
            return False, f"❌ Username already exists in {role}!"

    # add new row
    new_row = {"username": username, "password": password, "name": name}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(file_path, index=False)

    return True, f" {role.capitalize()} registered successfully!"
