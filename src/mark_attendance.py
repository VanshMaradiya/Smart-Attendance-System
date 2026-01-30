import os
import cv2
import pandas as pd
from datetime import datetime

from config import (ATTENDANCE_DIR, TRAINER_DIR, UNKNOWN_DIR,
                    FRONTAL_DEFAULT_XML, FRONTAL_ALT2_XML, PROFILE_XML,
                    OFFICE_START_TIME)


def detect_faces_3cascades(gray, c1, c2, c3):
    faces = c1.detectMultiScale(gray,
                                scaleFactor=1.2,
                                minNeighbors=5,
                                minSize=(80, 80))
    if len(faces) == 0:
        faces = c2.detectMultiScale(gray,
                                    scaleFactor=1.2,
                                    minNeighbors=5,
                                    minSize=(80, 80))
    if len(faces) == 0:
        faces = c3.detectMultiScale(gray,
                                    scaleFactor=1.2,
                                    minNeighbors=5,
                                    minSize=(80, 80))
    return faces


def get_today_file_path():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(ATTENDANCE_DIR, f"{today}.csv")


def is_already_marked(file_path: str, name: str) -> bool:
    if not os.path.exists(file_path):
        return False

    df = pd.read_csv(file_path)
    if "Name" not in df.columns:
        return False

    return name.lower() in df["Name"].astype(str).str.lower().values


def get_status(current_time_str: str) -> str:
    current_time = datetime.strptime(current_time_str, "%H:%M").time()
    office_time = datetime.strptime(OFFICE_START_TIME, "%H:%M").time()

    if current_time > office_time:
        return "Late"
    return "On Time"


def mark_attendance(name: str):
    file_path = get_today_file_path()

    if is_already_marked(file_path, name):
        print(f"Attendance already marked for {name} today ")
        return

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    status = get_status(time_str)

    row = {"Name": name, "Date": date_str, "Time": time_str, "Status": status}

    if not os.path.exists(file_path):
        df = pd.DataFrame([row])
        df.to_csv(file_path, index=False)
    else:
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df.to_csv(file_path, index=False)

    print(f" Attendance marked: {name} | {time_str} | {status}")
    print(f"Saved in: {file_path}")


def save_unknown_face(frame):
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"unknown_{ts}.jpg"
    save_path = os.path.join(UNKNOWN_DIR, file_name)
    cv2.imwrite(save_path, frame)
    print(f"Unknown person saved: {save_path}")


def main():
    #  Check xml files
    for xml_path in [FRONTAL_DEFAULT_XML, FRONTAL_ALT2_XML, PROFILE_XML]:
        if not os.path.exists(xml_path):
            print(" Cascade not found:", xml_path)
            print(" Put xml files inside models folder")
            return

    #  Load cascades
    cascade1 = cv2.CascadeClassifier(FRONTAL_DEFAULT_XML)
    cascade2 = cv2.CascadeClassifier(FRONTAL_ALT2_XML)
    cascade3 = cv2.CascadeClassifier(PROFILE_XML)

    #  Load trained model
    model_path = os.path.join(TRAINER_DIR, "trainer.yml")
    if not os.path.exists(model_path):
        print(" trainer.yml not found! Please run train_model.py first.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)

    #  Load labels mapping
    labels_path = os.path.join(TRAINER_DIR, "labels.txt")
    if not os.path.exists(labels_path):
        print(" labels.txt not found!")
        print(" Run train_model.py again (it will create labels.txt)")
        return

    id_name_map = {}
    with open(labels_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(",")
                if len(parts) == 2:
                    pid = int(parts[0])
                    pname = parts[1]
                    id_name_map[pid] = pname

    #  Start camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(" Camera not opening")
        return

    print(" Camera started. Press 'q' to quit.")

    last_marked_name = None
    last_action_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print(" Failed to read from camera")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #  Detect using 3 cascades
        faces = detect_faces_3cascades(gray, cascade1, cascade2, cascade3)

        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]

            label_id, confidence = recognizer.predict(face_roi)

            threshold = 70  # adjust for accuracy

            if confidence < threshold and label_id in id_name_map:
                name = id_name_map[label_id]

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{name} ({int(confidence)})", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                #  avoid repeated action in 10 sec
                current_time = datetime.now().timestamp()

                if (name != last_marked_name) or (current_time -
                                                  last_action_time > 10):
                    mark_attendance(name)
                    last_marked_name = name
                    last_action_time = current_time

            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                current_time = datetime.now().timestamp()
                if current_time - last_action_time > 10:
                    save_unknown_face(frame)
                    last_action_time = current_time

        cv2.imshow("Smart Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
