import json
import os
from .istorage import IStorage
from utils import safe_float, safe_str, safe_int


class StorageJson(IStorage):
    """
    JSON-based implementation of the IStorage interface.
    Stores and manages movie data in a JSON file.
    """

    def __init__(self, file_path):
        # Fügt "data/" vor dem Dateinamen ein
        self.file_path = os.path.join("data", file_path)
        # Erstellt den Ordner "data", falls nicht vorhanden
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        # Erstellt die JSON-Datei mit leerem Dict, falls nicht vorhanden
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding="utf-8") as f:
                json.dump({}, f)


    def list_movies(self):
        """Lists the movies stored in the json file to print it"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)

            return {
                title: {
                    "year": safe_int(data.get("year")),
                    "rating": safe_float(data.get("rating")),
                    "poster": safe_str(data.get("poster")),
                    "note": data.get("note", "")
                }
                for title, data in raw_data.items()
            }
        except FileNotFoundError:
            print(f"Warning: {self.file_path} not found.")
            return {}
        except json.JSONDecodeError:
            print("Error: Could not decode JSON.")
            return {}


    def add_movie(self, title, year, rating, poster):
        """Adds a new movie to the json file"""
        movies = self.list_movies()
        if title in movies:
            raise ValueError(f"Movie '{title}' already exists!")
        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster
        }
        self.save_movies(movies)


    def delete_movie(self, title):
        """Deletes a move from the json file, chosen by user input of the title."""
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self.save_movies(movies)


    def save_movies(self, movies):
        """Saves new data instantly with flush to the json file to ensure new data
        on the generated web page.
        """
        with open(self.file_path, 'w', encoding="utf-8") as f:
            json.dump(movies, f, indent=4)
            f.flush()
