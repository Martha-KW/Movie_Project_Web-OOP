import json
import os
from hashlib import sha256

class UserManager:
    USERS_FILE = os.path.join("data", "users.json")

    def __init__(self):
        """
        Initializes the user manager by loading existing users
        from a JSON file or creating a new end empty one if it doesn't exist.
        """

        if not os.path.exists(self.USERS_FILE):
            with open(self.USERS_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f)
        with open(self.USERS_FILE, "r", encoding="utf-8") as f:
            self.users = json.load(f)


    def _save_users(self):
        """Saves the current user dict to a json file"""
        with open(self.USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.users, f, indent=2)


    def hash_password(self, password):
        """Hashes the password text from user input with SHA-256 for safety"""
        return sha256(password.encode()).hexdigest()


    def create_user(self):
        """
        Registration of a new user. Prompts the user name input, file format and
        password. Stores the choices in the users.json file.
        """
        print("--- Create New User ---")
        while True:
            username = input("Choose a username: ").strip().lower()
            if username in self.users:
                print("Username already taken. Try another one.")
            else:
                break

        while True:
            format_choice = input("Choose storage format (json/csv): ").strip().lower()
            if format_choice in ["json", "csv"]:
                break
            else:
                print("Invalid format. Choose 'json' or 'csv'.")

        password = input("Choose a password: ").strip()
        password_hash = self.hash_password(password)

        file_name = f"{username}.{format_choice}"

        self.users[username] = {
            "password_hash": password_hash,
            "format": format_choice,
            "file": file_name
        }
        self._save_users()

        print(f"User '{username}' created successfully.\n")
        return username, format_choice, file_name


    def login_user(self):
        """
        Manages login for existing users. Checks if username exists, and if password is
        correct.
        """
        print("--- Login ---")
        username = input("Enter your username: ").strip().lower()
        if username not in self.users:
            print("User not found.")
            return None

        password = input("Enter your password: ").strip()
        if self.hash_password(password) != self.users[username]["password_hash"]:
            print("Incorrect password.")
            return None

        print(f"Welcome back, {username}!\n")
        user_data = self.users[username]
        return username, user_data["format"], user_data["file"]
