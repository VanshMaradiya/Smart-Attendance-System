import os
import cv2
import numpy as np
from datetime import datetime

from config import DATASET_DIR, TRAINER_DIR, FACE_SIZE


# ---------------------------------------------------------
# ✅ Read all dataset images and create:
# faces   -> list of face images (gray resized)
# labels  -> list of label ids (0,1,2...)
# id_name_map -> id to person name mapping
# ---------------------------------------------------------
def get_images_and_labels():
    """
    Expected dataset structure:

    dataset/
        Vansh/
            1.jpg
            2.jpg
        Rahul/
            1.jpg
            2.jpg
    """
    if not os.path.exists(DATASET_DIR):
        raise FileNotFoundError(f"❌ Dataset folder not found: {DATASET_DIR}")

    # ✅ get only folders (person names)
    persons = [d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))]
    persons.sort()

    if not persons:
        raise Exception("❌ No person folders found in dataset. Register faces first!")

    faces = []
    labels = []
    id_name_map = {}

    total_skipped = 0

    for pid, person_name in enumerate(persons):
        person_dir = os.path.join(DATASET_DIR, person_name)
        images = os.listdir(person_dir)

        # ✅ ignore empty folders
        if len(images) == 0:
            print(f"⚠️ Skipping empty folder: {person_name}")
            continue

        # ✅ save mapping
        id_name_map[pid] = person_name

        for img_name in images:
            img_path = os.path.join(person_dir, img_name)

            # ✅ only allow valid image formats
            if not img_name.lower().endswith((".png", ".jpg", ".jpeg")):
                total_skipped += 1
                continue

            img = cv2.imread(img_path)
            if img is None:
                print(f"⚠️ Unreadable image skipped: {img_path}")
                total_skipped += 1
                continue

            # ✅ convert to gray
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # ✅ resize image for same training quality
            gray = cv2.resize(gray, FACE_SIZE)

            faces.append(gray)
            labels.append(pid)

    if len(faces) == 0:
        raise Exception("❌ No valid face images found. Please register faces again!")

    print(f"✅ Total skipped images: {total_skipped}")
    return faces, labels, id_name_map


# ---------------------------------------------------------
# ✅ Save labels file
# format:
# 0,Vansh
# 1,Rahul
# ---------------------------------------------------------
def save_labels_file(id_name_map: dict):
    os.makedirs(TRAINER_DIR, exist_ok=True)

    labels_path = os.path.join(TRAINER_DIR, "labels.txt")
    with open(labels_path, "w", encoding="utf-8") as f:
        for pid, name in id_name_map.items():
            f.write(f"{pid},{name}\n")

    print(f"✅ labels.txt saved at: {labels_path}")


# ---------------------------------------------------------
# ✅ Main training function
# ---------------------------------------------------------
def main():
    print("\n" + "=" * 60)
    print("🔄 SMART ATTENDANCE SYSTEM - MODEL TRAINING STARTED")
    print("=" * 60)

    try:
        faces, labels, id_name_map = get_images_and_labels()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return

    # ✅ minimum images check (for accuracy)
    if len(faces) < 10:
        print("\n⚠️ Not enough images to train model properly.")
        print("✅ Please register at least 10-20 images per person.")
        return

    # ✅ display summary
    print("\n📌 TRAINING SUMMARY")
    print(f"✅ Total Persons: {len(id_name_map)}")
    print(f"✅ Total Face Images: {len(faces)}")
    print("✅ Persons List:", ", ".join(id_name_map.values()))

    # ✅ Train LBPH Model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))

    # ✅ Save trainer.yml
    os.makedirs(TRAINER_DIR, exist_ok=True)
    model_path = os.path.join(TRAINER_DIR, "trainer.yml")
    recognizer.save(model_path)

    print(f"\n✅ Model saved successfully: {model_path}")

    # ✅ Save labels mapping
    save_labels_file(id_name_map)

    print("\n✅ Training completed successfully 🎉")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
