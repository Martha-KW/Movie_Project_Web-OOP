from flask import Flask, render_template
from movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from user_manager import UserManager

app = Flask(__name__)


@app.route('/')
def index():
    user_manager = UserManager()

    # Fallback, wenn keine User existieren
    if not user_manager.users:
        return "No users found. Please register first."

    # Dynamisch: Nutze den ersten User in der users.json
    username = next(iter(user_manager.users))
    user_data = user_manager.users[username]
    file_type = user_data["format"]
    file_name = user_data["file"]  # z. B. "john.json" (ohne "data/")

    try:
        if file_type == "json":
            storage = StorageJson(file_name)
        else:
            storage = StorageCsv(file_name)
    except FileNotFoundError:
        return f"Error: {file_name} not found in data/ directory."

    movie_app = MovieApp(storage)
    movies = movie_app.get_movies()  # Annahme: Methode existiert in MovieApp

    return render_template("index.html", movies=movies)


if __name__ == "__main__":
    app.run(debug=True)
