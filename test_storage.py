from storage_json import StorageJson

# Create storage instance with a test file
storage = StorageJson("test_movies.json")

# Add a movie
storage.add_movie("Inception", 2010, 8.8, "https://example.com/inception.jpg")

# List movies
print("Movies after adding Inception:")
print(storage.list_movies())

# Update the movie
storage.update_movie("Inception", 9.0)
print("\nMovies after updating rating:")
print(storage.list_movies())

# Delete the movie
storage.delete_movie("Inception")
print("\nMovies after deleting Inception:")
print(storage.list_movies())
