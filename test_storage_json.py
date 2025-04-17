import os
import json
from storage_json import StorageJson

def test_add_and_list_movie(tmp_path):
    test_file = tmp_path / "test_movies.json"
    storage = StorageJson(test_file)

    # Add a movie
    storage.add_movie("Inception", 2010, 8.8, "http://poster.url")

    # Check if it's listed
    movies = storage.list_movies()
    assert "Inception" in movies
    assert movies["Inception"]["year"] == 2010
    assert movies["Inception"]["rating"] == 8.8
    assert movies["Inception"]["poster"] == "http://poster.url"

def test_update_movie(tmp_path):
    test_file = tmp_path / "test_movies.json"
    storage = StorageJson(test_file)

    storage.add_movie("Matrix", 1999, 9.0, "http://matrix.poster")
    storage.update_movie("Matrix", 9.5)

    movies = storage.list_movies()
    assert movies["Matrix"]["rating"] == 9.5


def test_update_nonexistent_movie(tmp_path, capsys):
    test_file = tmp_path / "test_movies.json"
    storage = StorageJson(test_file)

    storage.update_movie("Nonexistent", 7.0)

    captured = capsys.readouterr()
    assert "not found" in captured.out
