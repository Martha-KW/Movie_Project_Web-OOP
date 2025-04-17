from omdb_client import OmdbClient

class MovieApp:
    def __init__(self, storage):
        """
        Initialize the movie app with a storage backend (e.g., JSON, CSV).
        """
        self._storage = storage
        self.omdb_client = OmdbClient()

    def _command_list_movies(self):
        """
        List all movies stored in the storage.
        """
        movies = self._storage.list_movies()
        for title, details in movies.items():
            print(f"{title} ({details['year']}) - Rating: {details['rating']}, Poster: {details['poster']}")

    def _command_add_movie(self):
        """
        Add a new movie based on user input.
        """
        title = input("Enter movie title: ")
        movie_data = self.omdb_client.fetch_movie(title)

        if not movie_data:
            input("Press Enter to continue.")
            return

        self._storage.add_movie(
            movie_data["title"],
            movie_data["year"],
            movie_data["rating"],
            movie_data["poster"]
        )
        print(f"Movie '{movie_data['title']}' added.")
        input("Press Enter to continue.")

    def _command_delete_movie(self):
        """
        Delete a movie based on user input.
        """
        title = input("Enter movie title to delete: ")
        self._storage.delete_movie(title)
        print(f"Movie '{title}' deleted.")

    def _command_update_movie(self):
        """
        Update a movie rating.
        """
        title = input("Enter movie title to update: ")
        movies = self._storage.list_movies()

        if title not in movies:
            print(f"Movie '{title}' doesn't exist!")
            input("Press Enter to continue.")
            return

        rating = float(input("Enter new rating: "))
        self._storage.update_movie(title, rating)
        print(f"Rating for '{title}' successfully updated.")
        input("Press Enter to continue.")

    def run(self):
        """
        Run the main menu loop.
        """
        commands = {
            "1": self._command_list_movies,
            "2": self._command_add_movie,
            "3": self._command_delete_movie,
            "4": self._command_update_movie,
            "5": exit
        }

        while True:
            print("\n== Movie App Menu ==")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Update movie")
            print("5. Exit")

            choice = input("Choose an option: ")
            command = commands.get(choice)

            if command:
                command()
            else:
                print("Invalid choice. Try again.")
