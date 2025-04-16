from movie_app import MovieApp
from storage_json import StorageJson

def main():
    # different user data possible her later
    storage = StorageJson("movies.json")
    app = MovieApp(storage)
    app.run()

if __name__ == "__main__":
    main()
