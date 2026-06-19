import json
from datetime import datetime

with open("attendance.json", "r") as f:
    data = json.load(f)

for date, people in data.items():

    print("\nDate :", date)

    for name, details in people.items():

        sessions = details["sessions"]

        first_entry = sessions[0]["entry"]
        last_exit = sessions[-1]["exit"]

        total_work = 0
        total_break = 0

        for session in sessions:

            duration = session["duration"]

            h, m, s = map(int, duration.split(":"))

            total_work += h * 3600 + m * 60 + s

        for i in range(len(sessions) - 1):

            exit_time = datetime.strptime(
                sessions[i]["exit"],
                "%H:%M:%S"
            )

            next_entry = datetime.strptime(
                sessions[i + 1]["entry"],
                "%H:%M:%S"
            )

            total_break += int(
                (next_entry - exit_time).total_seconds()
            )

        print("Name :", name)
        print("First Entry :", first_entry)
        print("Last Exit :", last_exit)

        print(
            "Break Taken :",
            total_break // 60,
            "minutes"
        )

        work_hours = total_work // 3600
        work_minutes = (total_work % 3600) // 60

        print(
            "Working Time :",
            work_hours, "hr",
            work_minutes, "min"
        )
