from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """Return a list of all users."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Return a list of all movies for a specific user."""
        pass

    @abstractmethod
    def add_user(self, user_id, user_data):
        """Add a new user."""
        pass

    @abstractmethod
    def add_movie(self, user_id, movie_data):
        """Add a new movie to a user's list."""
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, updated_data):
        """Update an existing movie for a user."""
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """Delete a movie from a user's list."""
        pass
