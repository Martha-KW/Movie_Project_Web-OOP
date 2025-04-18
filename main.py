from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv
from user_manager import UserManager

def main():
    user_manager = UserManager()
    print("Welcome to the Movie App!\n")

    user_data = None

    while True:
        choice = input("Do you want to (1) Login or (2) Register? ").strip()
        if choice == "1":
            user_data = user_manager.login_user()
            if user_data:
                break  # successful login breaks the loop
        elif choice == "2":
            username, file_type, file_name = user_manager.create_user()
            user_data = (username, file_type, file_name)
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    # unpack user data
    username, file_type, file_name = user_data

    # Create appropriate storage object
    if file_type == "json":
        storage = StorageJson(file_name)
    elif file_type == "csv":
        storage = StorageCsv(file_name)
    else:
        print("Unknown storage type. Exiting.")
        return

    print(f"Welcome, {username}! Loading your movie data from {file_name}...\n")

    app = MovieApp(storage)
    app.run()

if __name__ == "__main__":
    main()
