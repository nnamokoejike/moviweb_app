import json
from moviweb_app.datamanager.data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        """Load data from the JSON file."""
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {self.filename} not found. Starting with an empty data structure.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.filename}. File may be corrupted.")
            return {}

    def save_data(self):
        """Save data to the JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_all_users(self):
        """Return a list of all users."""
        return self.data

    def get_user_movies(self, user_id):
        """Return a list of all movies for a specific user."""
        user_data = self.data.get(str(user_id))
        return user_data["movies"] if user_data else {}

    def add_user(self, user_id, user_data):
        """Add a new user."""
        self.data[str(user_id)] = {"name": user_data["name"], "movies": {}}
        self.save_data()

    def add_movie(self, user_id, movie_data):
        """Add a new movie to a user's list."""
        user = self.data.get(str(user_id))
        if user:
            movie_id = str(len(user["movies"]) + 1)   # Generate a unique movie ID
            user["movies"][movie_id] = movie_data
            self.save_data()

    def update_movie(self, user_id, movie_id, updated_data):
        """Update an existing movie for a user."""
        user = self.data.get(str(user_id))
        if user and movie_id in user["movies"]:
            user["movies"][movie_id].update(updated_data)
            self.save_data()

    def delete_movie(self, user_id, movie_id):
        """Delete a movie from a user's list."""
        user = self.data.get(str(user_id))
        if user and movie_id in user["movies"]:
            del user["movies"][movie_id]
            self.save_data()