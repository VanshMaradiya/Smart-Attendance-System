import os
import cv2

from config import (
    DATASET_DIR,
    FRONTAL_DEFAULT_XML,
    FRONTAL_ALT2_XML,
    PROFILE_XML,
    FACE_SIZE
)


def detect_faces_3cascades(gray, c1, c2, c3):
    """
    Try face detection with 3 cascades.
    Priority:
      1) frontal_default
      2) frontal_alt2
      3) profile_face
    """
    faces = c1.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))
    if len(faces) == 0:
        faces = c2.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))
    if len(faces) == 0:
        faces = c3.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))
    return faces


def register_face(person_name: str, max_images: int = 30):
    """
    Saves cropped face images into:
    dataset/PersonName/1.jpg ...
    """

    # ✅ Check xml files
    for xml_path in [FRONTAL_DEFAULT_XML, FRONTAL_ALT2_XML, PROFILE_XML]:
        if not os.path.exists(xml_path):
            print("❌ Cascade not found:", xml_path)
            print("✅ Put xml files inside models folder")
            return

    # ✅ Load cascades
    cascade1 = cv2.CascadeClassifier(FRONTAL_DEFAULT_XML)
    cascade2 = cv2.CascadeClassifier(FRONTAL_ALT2_XML)
    cascade3 = cv2.CascadeClassifier(PROFILE_XML)

    # ✅ Create person folder
    person_dir = os.path.join(DATASET_DIR, person_name)
    os.makedirs(person_dir, exist_ok=True)

    # ✅ Start camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not opening")
        return

    print(f"✅ Registration started for: {person_name}")
    print(f"📂 Saving images to: {person_dir}")
    print("👉 Press 'q' to stop early")

    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera frame not received")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ✅ Detect using 3 cascades
        faces = detect_faces_3cascades(gray, cascade1, cascade2, cascade3)

        for (x, y, w, h) in faces:
            # rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # crop face
            face_roi = gray[y:y + h, x:x + w]
            face_roi = cv2.resize(face_roi, FACE_SIZE)

            count += 1
            img_path = os.path.join(person_dir, f"{count}.jpg")
            cv2.imwrite(img_path, face_roi)

            print(f"✅ Saved {count}/{max_images}: {img_path}")

            # slow save speed
            cv2.waitKey(200)

            if count >= max_images:
                break

        # show info
        cv2.putText(frame, f"Person: {person_name}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.putText(frame, f"Images: {count}/{max_images}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Register Face - Smart Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("⚠️ Registration stopped by user.")
            break

        if count >= max_images:
            print("✅ Registration completed successfully 🎉")
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    print("\n===== Smart Attendance | Face Registration =====\n")

    person_name = input("Enter Employee Name: ").strip()
    if not person_name:
        print("❌ Name cannot be empty!")
        return

    register_face(person_name, max_images=30)


if __name__ == "__main__":
    main()
