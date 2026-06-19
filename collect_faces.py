import os
import cv2
name = input("Enter name: ")  

save_path = f"dataset/{name}"
os.makedirs(save_path, exist_ok=True)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

camera = cv2.VideoCapture(0)

count = 0

while True:
    success, frame = camera.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1

        face = gray[y:y+h, x:x+w]

        file_name = f"{save_path}/{count}.jpg"
        cv2.imwrite(file_name, face)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("Collecting Faces", frame)

    if cv2.waitKey(1) == 27 or count >= 50:  
        break

camera.release()
cv2.destroyAllWindows()
