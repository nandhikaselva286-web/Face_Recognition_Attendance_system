import cv2
import os
import json
from datetime import datetime

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

names = os.listdir("dataset")

logo = cv2.imread("Logo1.png", 0)

status = {}
entry_time = {}
last_scan = {}

COOLDOWN = 15

try:
    with open("attendance.json", "r") as f:
        data = json.load(f)
except:
    data = {}
    
def check_logo(frame_gray):
    result = cv2.matchTemplate(frame_gray, logo, cv2.TM_CCOEFF_NORMED)
    return cv2.minMaxLoc(result)[1] > 0.35

camera = cv2.VideoCapture(0)

while True:

    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]
        id_, confidence = recognizer.predict(face)

        if confidence < 70:

            name = names[id_]
            current_time = datetime.now()

            if name in last_scan:
              if (current_time - last_scan[name]).total_seconds() < COOLDOWN:
                continue

            if name not in status or status[name] == "OUT":

                if check_logo(gray):

                    status[name] = "IN"
                    entry_time[name] = current_time
                    last_scan[name] = current_time

                    print(name, "ENTERED AT : ", current_time.strftime("%H:%M:%S"))

                    cv2.putText(frame, "Please Enter", (x, y+h+25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

                else:

                    cv2.putText(frame, "Access denied", (x, y+h+25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

            else:

                duration = datetime.now() - entry_time[name]

                status[name] = "OUT"
                last_scan[name] = current_time

                print(name, "EXITED AT : ", current_time.strftime("%H:%M:%S"))
                print("Time spent : ", duration)
                print("Thank you !have a good day.")
                date = current_time.strftime("%d-%m-%Y")

                if date not in data:
                    data[date] = {}

                if name not in data[date]:
                    data[date][name] = {
                        "sessions": []
                        }

                data[date][name]["sessions"].append({
                  "entry": entry_time[name].strftime("%H:%M:%S"),
                  "exit": current_time.strftime("%H:%M:%S"),
                  "duration": str(duration).split(".")[0]
                })

                with open("attendance.json", "w") as f:
                     json.dump(data, f, indent=4)
        else:
            name = "Unknown"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.putText(frame, name, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Face + Uniform Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
