from movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from user_manager import UserManager

def main():
    """This manages the initial user interaction: login or register.
    For a new user it creates a new json or csv file as chosen.
    Then it initializes the movie app and the loop.
    """
    user_manager = UserManager()
    print("Welcome to the Movie App!\n")

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

    app = MovieApp(storage, username)
    app.run()

if __name__ == "__main__":
    main()
