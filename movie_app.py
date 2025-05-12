from omdb_client import OmdbClient
import statistics
import random

class MovieApp:
    def __init__(self, storage, username):
        """
        Initialize the movie app with a storage backend (e.g., JSON, CSV).
        """
        self._storage = storage
        self.omdb_client = OmdbClient()
        self.username = username


    def _command_list_movies(self):
        """
        List all movies stored in the storage.
        """
        movies = self._storage.list_movies()
        for title, details in movies.items():
            note = details.get("note", "")
            note_str = f"Note: {note}" if note else ""

            print(f"\n{title} ({details['year']})\n"
                  f"  Rating: {details['rating']}\n"
                  f"  Poster: {details['poster']}")
            if note_str:
                print(f"  {note_str}")
            print("-" * 40)


    def get_movies(self):
        return self._storage.list_movies()


    def _command_add_movie(self):
        """
        Add a new movie based on user input.
        """
        title = input("Enter movie title: ")
        movie_data = self.omdb_client.fetch_movie(title)

        if not movie_data:
            input("Press Enter to continue.")
            return
        rating = movie_data.get("rating") or 0.0
        try:
            self._storage.add_movie(
                movie_data["title"],
                movie_data["year"],
                movie_data["rating"],
                movie_data["poster"]
            )
            print(f"Movie '{movie_data['title']}' added.")
        except ValueError as e:
            print("This movie already exists.")
        input("Press Enter to continue.")


    def _command_delete_movie(self):
        """
        Delete a saved movie based on user input.
        """
        title_input = input("Enter the movie title to delete: ").strip().lower()
        movies = self._storage.list_movies()

        # Search case-insensitive und remove whitespace
        found_title = None
        for stored_title in movies:
            if stored_title.lower().strip() == title_input:
                found_title = stored_title
                break

        if not found_title:
            print(f"Movie '{title_input}' not found.")
            return

        self._storage.delete_movie(found_title)
        print(f"Movie '{found_title}' deleted.")
        input("Press Enter to continue.")


    def _command_update_movie(self):
        """
        Adds a personal comment to a movie and optionally updates rating.
        """
        title_input = input("Enter the movie title to add a note: ").strip().lower()
        movies = self._storage.list_movies()

        found_title = None
        for title in movies:
            if title.lower() == title_input:
                found_title = title
                break

        if not found_title:
            print(f"Movie '{title_input}' not found. Adding a note is impossible.")
            return

        note = input("Enter your note for the movie: ").strip()
        movies[found_title]["note"] = note
        self._storage.save_movies(movies)
        print(f"Note for '{found_title}' added successfully!")

        input("Press Enter to continue.")


    def _command_show_stats(self):
        """Generates statistical info about the saved movies. Median and average rating,
        the best and the worst movie. Ignores Movies without stats.
        """
        movies = self._storage.list_movies()

        # include only movies with a rating
        rated_movies = {title: data for title, data in movies.items()
                        if isinstance(data.get("rating"), (int, float))}

        if not rated_movies:
            print("No movies with ratings to analyze.")
            return

        ratings = [data["rating"] for data in rated_movies.values()]

        avg = statistics.mean(ratings)
        median = statistics.median(ratings)

        max_rating = max(rated_movies.items(), key=lambda item: item[1]["rating"])[1]["rating"]
        min_rating = min(rated_movies.items(), key=lambda item: item[1]["rating"])[1]["rating"]

        best_movies = [title for title, data in rated_movies.items() if
                       data["rating"] == max_rating]
        worst_movies = [title for title, data in rated_movies.items() if
                        data["rating"] == min_rating]

        print(f"\nAverage rating: {avg:.2f}")
        print(f"Median rating: {median:.2f}")
        print("Best movie(s):")
        print('\n'.join(f"- {movie}, {max_rating:.2f}" for movie in
                        best_movies))
        print("\nWorst movie(s):")
        print('\n'.join(f"- {movie}, {min_rating:.2f}" for movie in worst_movies))
        input("\nPress enter to continue.")


    def _command_random_movie(self):
        """Takes one random movie from the saved ones and displays it to the user."""

        movies = self._storage.list_movies()
        if not movies:
            print("No movies available.")
            return
        title, data = random.choice(list(movies.items()))
        print(f"Your movie for tonight: {title}, it's rated {data['rating']}")


    def _command_search_movie(self):
        query = input("Enter part of movie name: ").lower()
        movies = self._storage.list_movies()
        found = False

        for title, data in movies.items():
            if query in title.lower():
                print(f"{title}, Rating: {data.get('rating', 'N/A')}")
                found = True

        if not found:
            print("No matching movies found.")

        input("Press enter to continue")


    def _command_sort_by_rating(self):
        movies = self._storage.list_movies()
        sorted_movies = sorted(
            ((title, data) for title, data in movies.items() if data["rating"] is not None),
            key=lambda item: item[1]["rating"],
            reverse=True
        )
        print("\nMovies sorted by rating:")
        for title, data in sorted_movies:
            print(f"{title}: {data['rating']}")
        input("\nPress enter to continue")


    def _command_generate_website(self):
        movies = self._storage.list_movies()

        print("🌐 Generating website...")

        # Lade das HTML-Template
        with open("templates/index_template.html", "r", encoding="utf-8") as f:
            template = f.read()

        # Generate the dynamic Page title
        template = template.replace("__TEMPLATE_TITLE__",
                                    f"{self.username.capitalize()}s personal 🎥 App")

        # Create the html code for personal page
        movie_items = []
        for title, data in movies.items():
            poster = data.get('poster', '')
            year = data.get('year', '')
            note = data.get('note', '')

            item = f"""
            <li>
            <div class="movie">
            <div class="tooltip">
            <img class="movie-poster" src="{poster}" alt="Poster of {title}" />
            <span class="tooltiptext">{note}</span>
            </div>
            <div class="movie-title">{title}</div>
            <div class="movie-year">{year}</div>
            <div class="movie-rating">⭐ {data.get('rating', 'N/A')}</div>
            </div>
            </li>
            """
            movie_items.append(item)

        movie_grid = "\n".join(movie_items)
        template = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

        # saves the generated html in static/index.html
        with open("static/index.html", "w", encoding="utf-8") as f:
            f.write(template)

        print("✅ Website generated! Open static/index.html in your browser.")


    def run(self):
        """
        Run the main menu loop.
        """
        commands = {
            "0": exit,
            "1": self._command_list_movies,
            "2": self._command_add_movie,
            "3": self._command_delete_movie,
            "4": self._command_update_movie,
            "5": self._command_show_stats,
            "6": self._command_random_movie,
            "7": self._command_search_movie,
            "8": self._command_sort_by_rating,
            "9": self._command_generate_website,
        }

        while True:
            print("********** My Movies Database **********")
            print("\nMenu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Update movie")
            print("5. Stats")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")
            print("9. Generate website")

            choice = input("Choose an option: ")
            command = commands.get(choice)

            if command:
                command()
            else:
                print("Invalid choice. Try again.")
