import json
import os
from istorage import IStorage


class StorageJson(IStorage):
    """
    JSON-based implementation of the IStorage interface.
    Stores and manages movie data in a JSON file.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def list_movies(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def add_movie(self, title, year, rating, poster):
        movies = self.list_movies()
        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster
        }
        self._save_movies(movies)

    def delete_movie(self, title):
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, rating):
        """Update the rating of an existing movie."""
        movies = self.list_movies()

        if title not in movies:
            print(f"Movie '{title}' not found. Cannot update rating.")
            return False

        movies[title]['rating'] = rating
        self._save_movies(movies)
        return True

    def _save_movies(self, movies):
        with open(self.file_path, 'w') as f:
            json.dump(movies, f, indent=4)
