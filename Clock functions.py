import datetime
import json
import os
import time

# Function to create a JSON file for each day of the week
def create_weekly_alarm_files():
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days_of_week:
        filename = f"{day.lower()}_alarms.json"
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                json.dump({}, f)

# Function to add an alarm for a specific day of the week
def add_alarm(day_of_week, user_id, alarm_time):
    filename = f"{day_of_week.lower()}_alarms.json"
    with open(filename, "r") as f:
        alarms = json.load(f)
    alarms[str(user_id)] = alarm_time
    with open(filename, "w") as f:
        json.dump(alarms, f)

# Function to check alarms every minute
def check_alarms():
    while True:
        current_day = datetime.datetime.now().strftime("%A").lower()
        filename = f"{current_day}_alarms.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                alarms = json.load(f)
            current_time = datetime.datetime.now().strftime("%H:%M")
            for user_id, alarm_time in alarms.items():
                if alarm_time == current_time:
                    print(f"Alarm for user {user_id} on {current_day} at {alarm_time}!")
        time.sleep(60)  # Check every minute

# Example usage
create_weekly_alarm_files()
add_alarm("Monday", 123456789, "08:00")
check_alarms()