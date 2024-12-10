import json
from moviweb_app.datamanager.data_manager_interface import DataManagerInterface


def validate_user_input(user_id):
    try:
        if not isinstance(user_id, int):
            raise ValueError(f"Invalid input: user_id must be integer, got {type(user_id).__name__}")
        return True  # Return True if validation is successful
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return False  # Return False if validation fails
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        """Load data from the JSON file.
        """
        try:
            with open(self.filename, 'r') as file:  # Read file from json database
                return json.load(file)  # Loads file into temporary memory
        except FileNotFoundError:
            print(f"File {self.filename} not found. Starting with an empty data structure.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.filename}. File may be corrupted.")
            return {}

    def _save_data(self):
        """Save data to the JSON file."""
        with open(self.filename, 'w') as file:  # Write file into the json database
            json.dump(self.data, file, indent=4)  # Dumps file into the main json file

    def get_all_users(self):
        """Return a list of all users."""
        return self.data

    def get_user_by_id(self, user_id):
        if validate_user_input(user_id):
            user_data = self.data.get(str(user_id))
            if user_data:
                return user_data
            else:
                print(f"No user found with ID {user_id}")
                return {}  # Return None for invalid input

    def get_user_movies(self, user_id):
        """Return a list of all movies for a specific user."""
        if not validate_user_input(user_id):
            return {}  # Stop execution if validation fails
        try:
            # Retrieve user data using get_user_by_id
            if self.get_user_by_id(user_id) is None:
                return {}
            user_data = self.get_user_by_id(user_id)
            if user_data:
                return user_data["movies"]
            else:
                return f"No movies found for user ID {user_id}"
        except KeyError:
            print(f"KeyError: Unable to find movies for user ID {user_id}")
            return {}
        except TypeError:
            print(f"KeyError: Invalid data structure for user ID {user_id}")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {}

    def add_user(self, user_data):
        """Add a new user with an auto-generated ID.
        The new user ID is one greater than the highest existing
        If no users exist, the ID will be 1.
        """

        # Ensure the user_data contains the 'name' key
        if "name" not in user_data:
            return "Invalid user data. Missing 'name' field."
        if user_data['name'] == "":
            return "User Name cannot be empty, please provide a valid input"
        # Generate a new ID by finding the highest existing ID
        for user_id, user_info in self.data.items():
            if user_info["name"] == user_data["name"]:
                return f"User '{user_data['name']}' already exists in the database."
        if self.data:
            new_id = max(map(int, self.data.keys())) + 1
        else:
            new_id = 1
        self.data[str(new_id)] = {"name": user_data["name"], "movies": {}}
        self._save_data()
        return f"User '{user_data['name']}' added successfully with ID {new_id}."

    def add_movie(self, user_id, movie_data):
        """Add a new movie to a user's list."""
        if not validate_user_input(user_id):
            return f"Invalid user ID: {user_id}"

        user = self.data.get(str(user_id))
        if not user:
            return f"No user found with ID {user_id}"

        # Validate movie_data for required fields and formats
        required_fields = {
            "name": str,
            "director": str,
            "year": int,
            "rating": float
        }
        missing_fields = []
        incorrect_fields = {}

        for field, expected_type in required_fields.items():
            if field not in movie_data or not movie_data[field]:
                missing_fields.append(field)
            elif not isinstance(movie_data[field], expected_type):
                incorrect_fields[field] = f"Expected {expected_type.__name__}, got {type(movie_data[field]).__name__}"
            elif field == "year" and (movie_data["year"] < 1000 or movie_data["year"] > 9999):
                incorrect_fields["year"] = "Year must be a 4-digit integer."

        if missing_fields:
            return f"Movie data is incomplete. Missing fields: {', '.join(missing_fields)}"
        if incorrect_fields:
            issues = ', '.join([f"{field}: {error}" for field, error in incorrect_fields.items()])
            return f"Movie data has invalid fields.issues: {issues}"

        # Add the movie
        movies = user.get("movies", {})
        for movie_id, movie in movies.items():
            if movie["name"].lower() == movie_data["name"].lower():
                return f"Movie '{movie_data['name']}' already exists in {user['name']}'s movie list."

        # Add the movie
        movie_id = str(len(movies) + 1)  # Generate a unique movie ID
        movies[movie_id] = movie_data
        self._save_data()
        return f"Movie '{movie_data['name']}' added successfully to user ID {user_id}."

    def update_movie(self, user_id, movie_id, updated_data):
        """Update an existing movie for a user."""
        # Validate user ID
        if not validate_user_input(user_id):
            return f"Invalid user ID: {user_id}"

        # Validate movie ID
        if not isinstance(movie_id, int):
            return f"Invalid movie ID: {movie_id}. Must be integer."

        # Check if user exists
        user = self.data.get(str(user_id))
        if not user:
            return f"No user found with ID {user_id}"

        # Check if the movie exists for the user
        movies = user.get("movies", {})
        movie_id_str = str(movie_id)
        if movie_id_str not in movies:
            return f"No movie found with ID {movie_id} for user ID {user_id}"

        # retrieve the current movie data
        current_movie_data = movies[movie_id_str]

        # Check if updated_data matches current data
        if updated_data == current_movie_data:
            return "No new data provided for update. The movie data remains unchanged."

        # Validate updated_data for required fields and formats
        required_fields = {
            "name": str,
            "director": str,
            "year": int,
            "rating": float
        }
        missing_fields = []
        incorrect_fields = {}

        for field, expected_type in required_fields.items():
            if field not in updated_data or not updated_data[field]:
                missing_fields.append(field)
            elif not isinstance(updated_data[field], expected_type):
                incorrect_fields[field] = f"Expected {expected_type.__name__}, got {type(updated_data[field]).__name__}"
            elif field == "year" and (updated_data["year"] < 1000 or updated_data["year"] > 9999):
                incorrect_fields["year"] = "Year must be a 4-digit integer."

        if missing_fields:
            return f"Updated movie data is incomplete. Missing fields: {', '.join(missing_fields)}"
        if incorrect_fields:
            issues = ', '.join([f"{field}: {error}" for field, error in incorrect_fields.items()])
            return f"Updated movie data has invalid fields. Issues: {issues}"

        # Check for duplicate movie names within the user's list (excluding the current movie being updated)
        for mid, movie in movies.items():
            if mid != movie_id_str and movie["name"].lower() == updated_data["name"].lower():
                return f"Movie '{updated_data['name']}' already exists in {user['name']}'s movie list."

        # Update the movie
        movies[movie_id_str].update(updated_data)
        self._save_data()
        return f"Movie ID {movie_id} updated successfully for the user ID {user_id}."

    def delete_user(self, user_id):
        """Delete a user and their associated movies."""
        # Validate user ID
        if not validate_user_input(user_id):
            return f"Invalid user ID: {user_id}. Must be an integer."

        # Check if user exists
        if str(user_id) not in self.data:
            return f"No user found with ID {user_id}"

        # Delete the user
        del self.data[str(user_id)]
        self._save_data()
        return f"User ID {user_id} and their associated movies have been successfully deleted."

    def delete_movie(self, user_id, movie_id):
        """Delete a movie from a user's list."""
        # Validate user ID
        if not validate_user_input(user_id):
            return f"Invalid user ID: {user_id}"

        # Validate movie ID
        if not isinstance(movie_id, int):
            return f"Invalid movie ID: {movie_id}. Must be an integer."

        # check if user exists
        user = self.data.get(str(user_id))
        if not user:
            return f"No user found with ID {user_id}"

        # Check if the movie exists for the user
        movies = user.get("movies", {})
        movie_id_str = str(movie_id)
        if movie_id_str not in movies:
            return f"No movie found with ID {movie_id} for user ID {user_id}"

        # Delete the movie
        del movies[movie_id_str]
        self._save_data()
        return f"Movie ID {movie_id} successfully deleted for user ID {user_id}."
