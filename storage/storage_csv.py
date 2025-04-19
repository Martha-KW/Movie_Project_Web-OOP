import csv
import os
from .istorage import IStorage
from utils import safe_float, safe_str, safe_int

class StorageCsv(IStorage):
    """
    CSV-based implementation of the IStorage interface.
    Stores and manages movie data in a CSV file.
    """

    def __init__(self, file_path):
        """Generates a file path and csv file if it is not already existing"""
        self.file_path = os.path.join("data", file_path)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', encoding="utf-8", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["title", "year", "rating", "poster"])
                writer.writeheader()


    def list_movies(self):
        """Generates the movie listing for printing it"""
        movies = {}
        with open(self.file_path, encoding="utf-8", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = safe_str(row.get("title", ""))
                movies[title] = {
                    "year": safe_int(row.get("year")),
                    "rating": safe_float(row.get("rating", "")),
                    "poster": safe_str(row.get("poster", "")),
                    "note": row.get("note", "")
                }
        return movies


    def add_movie(self, title, year, rating, poster):
        """Adds a new movie to the csv file"""
        movies = self.list_movies()
        if title in movies:
            print(f"Movie '{title}' already exists.")
            return
        with open(self.file_path, mode='a', encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["title", "year", "rating", "poster"])
            writer.writerow({
                "title": title,
                "year": year,
                "rating": rating,
                "poster": poster
            })


    def delete_movie(self, title):
        """
        Deletes a movie by title (case-insensitive search) from csv file.
        """
        movies = self.list_movies()

        found_title = None
        for stored_title in movies:
            if stored_title.lower().strip() == title.lower().strip():
                found_title = stored_title
                break

        if not found_title:
            print(f"Movie '{title}' not found.")
            return

        del movies[found_title]
        self.save_movies(movies)


    def save_movies(self, movies):
        """Saves the movie data collected from omdb to the csv file and writes
        instantly with flush to generate the website with new content.
        """
        with open(self.file_path, mode='w', encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["title", "year", "rating", "poster",
                                                   "note" ])
            writer.writeheader()
            for title, data in movies.items():
                writer.writerow({
                    "title": title,
                    "year": data["year"] if data["year"] is not None else "",
                    "rating": data["rating"] if data["rating"] is not None else "",
                    "poster": safe_str(data.get("poster", "")),
                    "note": data.get("note", "")
                })
            f.flush()
