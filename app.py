from flask import Flask, render_template
from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv
from user_manager import UserManager

app = Flask(__name__)

@app.route('/')
def index():
    # Hier kommt dein Code, um den richtigen Benutzer zu holen
    user_manager = UserManager()
    username = "john"  # Dies könnte dynamisch aus einem Login oder einer Session kommen
    file_type = "json"  # Beispiel, je nach Benutzer
    file_name = f"{username}.{file_type}"

    if file_type == "json":
        storage = StorageJson(file_name)
    else:
        storage = StorageCsv(file_name)

    app = MovieApp(storage)

    # Holen der Filmdaten für die Anzeige
    movies = app.get_movies()  # Hier geht es davon aus, dass MovieApp eine Methode `get_movies()` hat.

    # Übergibt die Filmdaten an das HTML Template
    return render_template("index.html", movies=movies)


if __name__ == "__main__":
    app.run(debug=True)
