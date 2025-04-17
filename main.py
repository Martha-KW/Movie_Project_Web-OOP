from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv

def main():
    # different user data possible her later
    # storage = StorageCsv("movies.csv")
    storage = StorageJson("movies.json")
    app = MovieApp(storage)
    app.run()

if __name__ == "__main__":
    main()
