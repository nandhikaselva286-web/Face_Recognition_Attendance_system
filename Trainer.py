import cv2
import os
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_id = 0
label_map = {}

for name in os.listdir("dataset"):
    path = os.path.join("dataset", name)

    if not os.path.isdir(path):
        continue

    label_map[label_id] = name

    for img_name in os.listdir(path):
        img_path = os.path.join(path, img_name)
        img = cv2.imread(img_path, 0)

        if img is None:
            continue

        faces.append(img)
        labels.append(label_id)

    label_id += 1

recognizer.train(np.array(faces, dtype="object"), np.array(labels))
recognizer.save("trainer.yml")

print("Done", label_map)
