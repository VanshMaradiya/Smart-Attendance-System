import argparse
import os
import pandas as pd
from datetime import datetime

from config import ATTENDANCE_DIR, TEAM_CSV


# ✅ Get file path by date
def attendance_file_by_date(date_str: str):
    """
    date_str format: YYYY-MM-DD
    returns file path: attendance/YYYY-MM-DD.csv
    """
    file_path = os.path.join(ATTENDANCE_DIR, f"{date_str}.csv")
    if os.path.exists(file_path):
        return file_path
    return None


# ✅ Get latest attendance file
def latest_attendance_file():
    if not os.path.exists(ATTENDANCE_DIR):
        return None

    files = [f for f in os.listdir(ATTENDANCE_DIR) if f.endswith(".csv")]
    if not files:
        return None

    files.sort(reverse=True)
    return os.path.join(ATTENDANCE_DIR, files[0])


# ✅ Load manager team members
def load_team_members(manager_name: str):
    if not os.path.exists(TEAM_CSV):
        return []

    df = pd.read_csv(TEAM_CSV)

    # safe columns check
    if "Manager" not in df.columns or "Employee" not in df.columns:
        return []

    team = df[df["Manager"].astype(str).str.lower() == manager_name.lower()]["Employee"].astype(str).tolist()
    return team


# ✅ Read multiple attendance files (range)
def read_attendance_range(from_date: str, to_date: str):
    """
    Read files from from_date to to_date.
    Returns combined dataframe.
    """
    start = datetime.strptime(from_date, "%Y-%m-%d")
    end = datetime.strptime(to_date, "%Y-%m-%d")

    if start > end:
        raise ValueError("from_date cannot be greater than to_date")

    all_data = []

    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        file_path = attendance_file_by_date(date_str)

        if file_path:
            df = pd.read_csv(file_path)
            df["File"] = os.path.basename(file_path)  # optional
            all_data.append(df)

        current = current + pd.Timedelta(days=1)

    if not all_data:
        return None

    return pd.concat(all_data, ignore_index=True)


def main():
    parser = argparse.ArgumentParser(description="View Attendance Report")
    parser.add_argument("--mode", choices=["all", "team", "self"], required=True)

    # For self mode
    parser.add_argument("--name", default="")

    # For team mode
    parser.add_argument("--manager", default="")

    # ✅ New options
    parser.add_argument("--date", default="", help="YYYY-MM-DD (view specific date attendance file)")
    parser.add_argument("--from_date", default="", help="YYYY-MM-DD (start date)")
    parser.add_argument("--to_date", default="", help="YYYY-MM-DD (end date)")

    args = parser.parse_args()

    # ✅ Decide which file to use
    df = None
    used_files = []

    try:
        if args.date:
            file_path = attendance_file_by_date(args.date)
            if not file_path:
                print(f"❌ No attendance file found for date: {args.date}")
                return

            df = pd.read_csv(file_path)
            used_files.append(file_path)

        elif args.from_date and args.to_date:
            df = read_attendance_range(args.from_date, args.to_date)
            if df is None:
                print(f"❌ No attendance files found between {args.from_date} to {args.to_date}")
                return

            used_files.append(f"{args.from_date} to {args.to_date}")

        else:
            # default latest
            file_path = latest_attendance_file()
            if not file_path:
                print("❌ No attendance file found.")
                return

            df = pd.read_csv(file_path)
            used_files.append(file_path)

    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # ✅ Apply mode filtering
    if args.mode == "all":
        print("\n✅ Showing ALL Attendance\n")
        print(df)

    elif args.mode == "self":
        if not args.name:
            print("❌ Please provide --name for self mode")
            return

        df_self = df[df["Name"].astype(str).str.lower() == args.name.lower()]
        print(f"\n✅ Showing Attendance for: {args.name}\n")
        print(df_self)

    elif args.mode == "team":
        if not args.manager:
            print("❌ Please provide --manager for team mode")
            return

        team = load_team_members(args.manager)
        if not team:
            print("⚠️ No team found for this manager. Add manager_teams.csv")
            return

        df_team = df[df["Name"].astype(str).isin(team)]
        print(f"\n✅ Showing TEAM Attendance for Manager: {args.manager}\n")
        print(df_team)

    # ✅ Show used file info
    print("\n📂 Files used:")
    for f in used_files:
        print(" -", f)


if __name__ == "__main__":
    main()
