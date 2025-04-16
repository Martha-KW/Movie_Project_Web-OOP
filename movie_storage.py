import json

MOVIE_DATA = "data.json"

def get_movies():
    """Imports movie data from data.json file"""
    try:
        with open(MOVIE_DATA, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_movies(movies):
    """Saves the movies in the json file"""
    with open(MOVIE_DATA, "w") as file:
        json.dump(movies, file, indent=4)

def add_movie(title, year, rating):
    """Adds a new movie and saves the tata to the json file"""
    movies = get_movies()
    movies[title] = {"year": int(year), "rating": float(rating)}
    save_movies(movies)

def delete_movie(title):
    """Deletes a movie and saves the rest of the data"""
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)

def update_movie(title, rating):
    """Updates the rating of a movie and saves the data."""
    movies = get_movies()
    if title in movies:
        movies[title]["rating"] = rating
        save_movies(movies)
