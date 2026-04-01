# file: main.py

import time
import json
from typing import List

LOG_FILE = "deception_logs.json"


class AlertSystem:
    def __init__(self):
        self.logs: List[dict] = []

    def log_event(self, event_type: str, description: str, suspicious: bool):
        entry = {
            "timestamp": time.ctime(),
            "event_type": event_type,
            "description": description,
            "suspicious": suspicious
        }
        self.logs.append(entry)
        self.save_logs()

        if suspicious:
            self.trigger_alert(entry)

    def trigger_alert(self, entry):
        print("\n🚨 ALERT: Suspicious Activity Detected!")
        print(f"Time: {entry['timestamp']}")
        print(f"Event: {entry['event_type']}")
        print(f"Details: {entry['description']}\n")

    def save_logs(self):
        with open(LOG_FILE, "w") as f:
            json.dump(self.logs, f, indent=4)

    def load_logs(self):
        try:
            with open(LOG_FILE, "r") as f:
                self.logs = json.load(f)
        except FileNotFoundError:
            self.logs = []

    def show_logs(self):
        for log in self.logs:
            print(log)


class DeceptionSystem:
    def __init__(self):
        self.alert_system = AlertSystem()
        self.failed_attempts = 0
        self.max_attempts = 3

    # -----------------------
    # FAKE LOGIN SYSTEM
    # -----------------------
    def fake_login(self):
        print("\n--- Secure Login Portal ---")
        username = input("Username: ")
        password = input("Password: ")

        # Always fake (honeypot)
        self.failed_attempts += 1

        self.alert_system.log_event(
            "LOGIN_ATTEMPT",
            f"Login attempt with username={username}",
            suspicious=True
        )

        if self.failed_attempts >= self.max_attempts:
            self.alert_system.log_event(
                "BRUTE_FORCE",
                "Multiple failed login attempts detected",
                suspicious=True
            )
            print("Account locked due to suspicious activity.\n")
        else:
            print("Invalid credentials.\n")

    # -----------------------
    # HONEYPOT FILE ACCESS
    # -----------------------
    def access_honeypot(self):
        print("\nAccessing confidential file...")

        self.alert_system.log_event(
            "HONEYPOT_ACCESS",
            "Unauthorized access to hidden file detected",
            suspicious=True
        )

        print("Access denied.\n")

    # -----------------------
    # NORMAL ACTION (CONTROL)
    # -----------------------
    def normal_action(self):
        print("\nPerforming normal system operation...")

        self.alert_system.log_event(
            "NORMAL_ACTIVITY",
            "User performed normal operation",
            suspicious=False
        )

        print("Operation completed.\n")

    # -----------------------
    # CLI MENU
    # -----------------------
    def run(self):
        self.alert_system.load_logs()

        while True:
            print("\n===== Deception Security System =====")
            print("1. Login")
            print("2. Access Confidential File")
            print("3. Normal Operation")
            print("4. View Logs")
            print("5. Exit")

            choice = input("Choose: ")

            if choice == "1":
                self.fake_login()

            elif choice == "2":
                self.access_honeypot()

            elif choice == "3":
                self.normal_action()

            elif choice == "4":
                self.alert_system.show_logs()

            elif choice == "5":
                break

            else:
                print("Invalid choice.")


if __name__ == "__main__":
    system = DeceptionSystem()
    system.run()