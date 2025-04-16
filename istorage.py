from abc import ABC, abstractmethod

class IStorage(ABC):
    """
    Interface that defines the contract for storage operations.
    Any storage class (e.g. JSON, CSV) must implement these methods.
    """

    @abstractmethod
    def list_movies(self):
        """Returns all stored movies as a dictionary."""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Adds a new movie to storage.

        Args:
            title (str): Title of the movie.
            year (int): Year of release.
            rating (float): Movie rating.
            poster (str): URL of the movie poster.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie by its title.

        Args:
            title (str): Title of the movie to delete.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Updates the rating of a movie.

        Args:
            title (str): Title of the movie.
            rating (float): New rating.
        """
        pass
