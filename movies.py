from statistics import median, mean
import random
from colorama import Fore, Style
from fuzzywuzzy import process, fuzz
import movie_storage


def get_non_empty_input(prompt):
    """This function helps to ensure that user input is never empty."""
    user_input = ""
    while not user_input.strip():
        user_input = input(prompt).strip()
    return user_input


def show_users_menue():
    """This function prints the starting menue, that will reappear after every round."""
    print("********** My Movies Database **********\n")
    print("Menu:")
    print(" 0. Exit")
    print(" 1. List movies")
    print(" 2. Add movie")
    print(" 3. Delete movie")
    print(" 4. Update movie")
    print(" 5. Stats")
    print(" 6. Random movie")
    print(" 7. Search movie")
    print(" 8. Movies sorted by rating")
    print(" 9. Movies sorted by year")
    print("10. Movies filtered by year and / or rating\n")


def list_movies(movies):
    """ This function prints all saved movies, their rating and year."""
    print("")
    print(Fore.GREEN + f"{len(movies)} movies in total: \n")
    for title, details in movies.items():
        year = details.get("year", "N/A")
        rating = details.get("rating", "N/A")
        print(f"{title} ({year}): {rating}")
    print("\n" + Style.RESET_ALL)
    return movies


def add_movies(movies):
    """ This function asks the user to add a new movie and checks if the movie already exists
    to avoid duplicates. It converts the rating to a float and asks for a year."""
    print("")
    title = get_non_empty_input("Enter new movie name: ").strip()
    movies = movie_storage.get_movies()
    if any(title.lower() == existing_title.lower() for existing_title in movies):
        print(Fore.RED + f"Movie {title} already exists!" + Style.RESET_ALL)
    else:
        year = get_non_empty_input("Enter new movie year: ")
        try:
            rating = float(get_non_empty_input("Enter new movie rating (0-10): "))
            if not 0 <= rating <= 10:
                raise ValueError("Rating has to be among 0 and 10!")
            movie_storage.add_movie(title, year, float(rating))
            print(f"Movie {title} successfully added\n")
        except ValueError as e:
            print(Fore.RED + f"Invalid Value for a rating: {e}" + Style.RESET_ALL)
    movies = movie_storage.get_movies()
    return movies


def delete_movie(movies):
    """ This function asks the user to choose one movie to delete from dict.
     It warns if the movie ist not in the dict."""
    print("")
    movie_to_delete = get_non_empty_input("Enter movie name to delete: ")
    if movie_to_delete in movies:
        movie_storage.delete_movie(movie_to_delete)
        print(f"Movie {movie_to_delete} successfully deleted")
        print("")
    else:
       print(Fore.RED + f"Movie {movie_to_delete} doesn't exist! \n" + Style.RESET_ALL)
    movies = movie_storage.get_movies()
    return movies


def update_movie(movies):
    """This function asks the user to update the rating of a movie that is already saved. It
    warns the user if the move is not included in the dict."""
    print("")
    movie_to_update = get_non_empty_input("Enter movie name: ")
    if movie_to_update in movies:
        try:
            updated_rating = float(get_non_empty_input("Enter new movie rating (0-10): "))
            if not 0 <= updated_rating <= 10:
                raise ValueError("Rating has to be among 0 and 10!")
            movie_storage.update_movie(movie_to_update, float(updated_rating))
            print(f"Movie {movie_to_update} successfully updated\n")
        except ValueError as e:
            print(Fore.RED + f"Invalid rating: {e}" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Movie {movie_to_update} doesn't exist!\n" + Style.RESET_ALL)
    movies = movie_storage.get_movies()
    return movies


def stats_movie(movies):
    """ This function prints out statistical information about the movies in the dict:
    Movies with the highest and lowest rating (all movies in case of ties)
    Average rating
    Median rating"""
    ratings = [details["rating"] for details in movies.values()]
    max_rating = max(ratings)
    min_rating = min(ratings)
    average_rated = mean(ratings)
    median_rating = median(ratings)
    best_rated = \
        [title for title, details in movies.items() if details["rating"] == max_rating]
    worst_rated = \
        [title for title, details in movies.items() if details["rating"] == min_rating]
    print("")
    print(f"Average rating: {average_rated:.2f}")
    print(f"Median rating: {median_rating:.2f}")
    print("")
    print("Best movie(s):")
    for movie in best_rated:
        print(f"{movie}: {max_rating}")
    print("")
    print("Worst movie(s):")
    for movie in worst_rated:
        print(f"{movie}: {min_rating}")
    return movies


def randomized_movie(movies):
    """This function prints out a random movie as a suggestion for the user."""
    print("")
    title, details = random.choice(list(movies.items()))
    print(f"Your movie for tonight: {title}, it's rated {details['rating']}")
    print("")
    return movies


def search_movie(movies):
    """This function allows the user to search if a movie is in the dict.
    If not, it warns the user. If a similar movie is contained, it
    gives a hint to the user."""
    print("")
    search_movie = get_non_empty_input("Enter part of movie name: ").strip().lower()
    check_database_containing_search = [f"{title}, {details["rating"]}"
                                        for title, details in movies.items() if
                                        search_movie in title.lower()]
    if check_database_containing_search:
        print("\n".join(check_database_containing_search))
    else:
        print(Fore.RED + f"Movie {search_movie} does not exist." + Style.RESET_ALL)
        similar_titles = (
            process.extract(search_movie, movies.keys(), limit=3, scorer=fuzz.ratio))
        if similar_titles:
            for title, score in similar_titles:
                if score >= 70:
                    print(f"Did you perhaps mean {title}?")
        else:
            print(Fore.RED + "No similar Movies found.")
    print("")
    return movies


def descending_sorted_movie(movies):
    """This function prints all the movies in the dict beginning with the highest rated in
    descending order for the user."""
    print("")
    movies_sorted = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    for title, details in movies_sorted:
        print(f"{title} ({details["year"]}): {details["rating"]}")
    return movies


def movies_sorted_by_year(movies):
    """THis function sorts the movies from the json file depending on the choice in user input
     and prints them. Yes prints newest movies first, no oldest movies first"""
    if not movies:
        print("No movies available.")
        return movies
    user_input = input("Do you want to see the latest movies first? (y/n): ").strip().lower()
    if user_input == "y":
        sorted_movies = sorted(movies.items(), key=lambda item: item[1]["year"], reverse=True)
    elif user_input == "n":
        sorted_movies = sorted(movies.items(), key=lambda item: item[1]["year"])
    else:
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")
        return movies
    print("\nMovies sorted by year:")
    for title, details in sorted_movies:
        print(f"{title} ({details['year']}): {details['rating']}")
    return movies


def filter_movies(movies):
    """Filters movies based on user-provided criteria."""
    if not movies:
        print("No movies available.")
        return movies
    try:
        min_rating = input("Enter minimum rating (or leave blank): "
                           "").strip()
        start_year = input("Enter start year (or leave blank): ").strip()
        end_year = input("Enter end year (or leave blank): ").strip()
        min_rating = float(min_rating) if min_rating else None
        start_year = int(start_year) if start_year else None
        end_year = int(end_year) if end_year else None
        filtered_movies = {
            title: details
            for title, details in movies.items()
            if (min_rating is None or details["rating"] >= min_rating)
            and (start_year is None or details["year"] >= start_year)
            and (end_year is None or details["year"] <= end_year)
        }
        if filtered_movies:
            print("\nFiltered Movies:")
            for title, details in filtered_movies.items():
                print(f"{title} ({details['year']}): {details['rating']}")
        else:
            print("No movies match the given criteria.")
        return movies
    except ValueError:
        print("Please enter numbers for the year and the rating!")


function_dispatcher = {
    "1": list_movies,
    "2": add_movies,
    "3": delete_movie,
    "4": update_movie,
    "5": stats_movie,
    "6": randomized_movie,
    "7": search_movie,
    "8": descending_sorted_movie,
    "9": movies_sorted_by_year,
    "10": filter_movies
}


def main():
    """ Here is the central point where all functions are controlled."""
    movies = movie_storage.get_movies()
    while True:
        show_users_menue()
        choice = get_non_empty_input("Enter choice (1-10): ")
        if choice in function_dispatcher:
            movies = function_dispatcher[choice](movies)
        elif choice == "0":
            print("Bye!\n")
            break
        else:
            print("Invalid input, try again!")
        input(Fore.MAGENTA + "Press enter to continue" + Style.RESET_ALL)


if __name__ == "__main__":
    main()