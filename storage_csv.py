import csv
import os
from istorage import IStorage

class StorageCsv(IStorage):
    """
    CSV-based implementation of the IStorage interface.
    Stores and manages movie data in a CSV file.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["title", "year", "rating", "poster"])
                writer.writeheader()

    def list_movies(self):
        movies = {}
        with open(self.file_path, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row["title"]
                movies[title] = {
                    "year": int(row["year"]),
                    "rating": float(row["rating"]),
                    "poster": row["poster"]
                }
        return movies

    def add_movie(self, title, year, rating, poster):
        movies = self.list_movies()
        if title in movies:
            print(f"Movie '{title}' already exists.")
            return
        with open(self.file_path, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["title", "year", "rating", "poster"])
            writer.writerow({
                "title": title,
                "year": year,
                "rating": rating,
                "poster": poster
            })

    def delete_movie(self, title):
        movies = self.list_movies()
        if title not in movies:
            print(f"Movie '{title}' not found.")
            return
        del movies[title]
        self._save_all_movies(movies)

    def update_movie(self, title, rating):
        movies = self.list_movies()
        if title not in movies:
            print(f"Movie '{title}' not found. Cannot update rating.")
            return
        movies[title]["rating"] = rating
        self._save_all_movies(movies)
        print(f"Updated rating for movie '{title}' to {rating}.")

    def _save_all_movies(self, movies):
        with open(self.file_path, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["title", "year", "rating", "poster"])
            writer.writeheader()
            for title, data in movies.items():
                writer.writerow({
                    "title": title,
                    "year": data["year"],
                    "rating": data["rating"],
                    "poster": data["poster"]
                })
