from omdb_client import OmdbClient
import statistics
import random

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
            note = details.get("note", "")
            note_str = f"Note: {note}" if note else ""

            print(f"\n{title} ({details['year']})\n"
                  f"  Rating: {details['rating']}\n"
                  f"  Poster: {details['poster']}")
            if note_str:
                print(f"  {note_str}")
            print("-" * 40)

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
        Delete a saved movie based on user input.
        """
        title_input = input("Enter the movie title to delete: ").strip().lower()
        movies = self._storage.list_movies()

        # Case-insensitive und Whitespace-bereinigt suchen
        found_title = None
        for stored_title in movies:
            if stored_title.lower().strip() == title_input:
                found_title = stored_title  # Behalte Original-Schreibweise!
                break

        if not found_title:
            print(f"Movie '{title_input}' not found.")
            return

        self._storage.delete_movie(found_title)  # Lösche mit Original-Schreibweise
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

        best = max(rated_movies.items(), key=lambda item: item[1]["rating"])
        worst = min(rated_movies.items(), key=lambda item: item[1]["rating"])

        print(f"\nAverage rating: {avg:.2f}")
        print(f"Median rating: {median:.2f}")
        print(f"Best movie: {best[0]}, {best[1]['rating']:.2f}")
        print(f"Worst movie: {worst[0]}, {worst[1]['rating']:.2f}")
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

        # Ersetze den Titel
        template = template.replace("__TEMPLATE_TITLE__", "My Movie App")

        # Baue das Movie-HTML
        movie_items = []
        for title, data in movies.items():  # <- das ist wichtig!
            item = f"""
            <li>
                <div class="movie">
                    <img class="movie-poster" src="{data.get('poster', '')}" />
                    <div class="movie-title">{title}</div>
                    <div class="movie-year">{data.get('year')}</div>
                </div>
            </li>
            """
            movie_items.append(item)

        movie_grid = "\n".join(movie_items)
        template = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

        # Speichere das Ergebnis in static/index.html
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
