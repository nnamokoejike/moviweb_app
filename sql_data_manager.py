from moviweb_app.datamanager.data_manager_interface import DataManagerInterface
from appORM import app, db, User, Movie, FavoriteMovies  # Import your User model


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_instance):
        self.db = db_instance

    def get_all_users(self):
        """Return a list of all users."""
        users = User.query.all()
        return users

    def get_user_movies(self, user_id):
        """Return a list of all movies for a specific user."""
        user = self.db.session.query(User).filter_by(user_id=user_id).first()
        if user:
            # Access the 'favorite_movies' relationship defined in your User model
            return user.favorite_movies
        return []  # Return an empty list if user not found

    def add_user(self, user_data):
        """Add a new user."""
        try:
            new_user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=user_data["password_hash"]
            )
            self.db.session.add(new_user)
            self.db.session.commit()
            print(f"User {new_user.username} added successfully with ID: {new_user.user_id}")
            return new_user.user_id
        except Exception as e:
            self.db.session.rollback()
            print(f"Error adding user: {e}")
            return None

    def add_movie(self, user_id, movie_data):
        """Add a new movie to a user's list."""
        try:
            # First, check if the user exists
            user = self.db.session.query(User).filter_by(user_id=user_id).first()
            if not user:
                print(f"Error: User with ID {user_id} not found.")
                return None

            # Check if the movie already exists by title or imdb_id
            existing_movie = self.db.session.query(Movie).filter_by(title=movie_data["title"]).first()
            if existing_movie:
                print(f"Movie '{movie_data['title']}' already exists. Associating existing movie with user.")
                movie_to_add = existing_movie
            else:
                # Create a new movie instance
                new_movie = Movie(
                    title=movie_data["title"],
                    year=movie_data["year"],
                    rating=movie_data["rating"],
                    director=movie_data["director"],
                    imdb_id=movie_data.get("imdb_id")  # Use .get for optional fields
                )
                self.db.session.add(new_movie)
                self.db.session.commit()  # Commit to get the movie_id if new
                print(f"Movie '{new_movie.title}' added to database with ID: {new_movie.movie_id}")
                movie_to_add = new_movie

            # Now, associate the movie with the user
            # Check if the association already exists to prevent duplicates in favorite_movies
            if movie_to_add not in user.favorite_movies:
                user.favorite_movies.append(movie_to_add)
                self.db.session.commit()
                print(f"Movie '{movie_to_add.title}' associated with user '{user.username}'.")
                return movie_to_add.movie_id
            else:
                print(f"Movie '{movie_to_add.title}' is already a favorite of user '{user.username}'.")
                return movie_to_add.movie_id  # Return existing movie ID

        except Exception as e:
            self.db.session.rollback()
            print(f"Error adding/associating movie: {e}")
            return None

    def update_movie(self, user_id, movie_id, updated_data):
        """Update an existing movie for a user."""
        try:
            # First, check if the user exists and if the movie is in their favorites
            user = self.db.session.query(User).filter_by(user_id=user_id).first()
            if not user:
                print(f"Error: User with ID {user_id} not found.")
                return False

            # Check if the movie is in the user's favorites
            movie_to_update = None
            for movie in user.favorite_movies:
                if movie.movie_id == movie_id:
                    movie_to_update = movie
                    break

            if not movie_to_update:
                print(f"Error: Movie with ID {movie_id} not found in user {user.username}\'s favorites.")
                return False

            # Update movie details from updated_data dictionary
            for key, value in updated_data.items():
                if hasattr(movie_to_update, key):
                    setattr(movie_to_update, key, value)
                else:
                    print(f"Warning: Movie model does not have attribute \'{key}\'.")

            self.db.session.commit()
            print(f"Movie ID {movie_id} updated successfully for user {user.username}.")
            return True
        except Exception as e:
            self.db.session.rollback()
            print(f"Error updating movie: {e}")
            return False

    def delete_movie(self, user_id, movie_id):
        """Delete a movie from a user's list."""
        try:
            user = self.db.session.query(User).filter_by(user_id=user_id).first()
            if not user:
                print(f"Error: User with ID {user_id} not found.")
                return False

            # Find the movie within the user's favorite_movies
            movie_to_remove = None
            for movie in user.favorite_movies:
                movie_to_remove = movie
                break

            if not movie_to_remove:
                print(f"Error: Movie with ID {movie_id} not found in user {user.username}\'s favorites.")
                return False

            user.favorite_movies.remove(movie_to_remove)
            self.db.session.commit()
            print(f"Movie '{movie_to_remove.title}' successfully removed from user {user.username}\'s favorites.")

            return True
        except Exception as e:
            self.db.session.rollback()
            print(f"Erro deleting movie: {e}")
            return False


if __name__ == '__main__':
    with app.app_context():
        data_manager = SQLiteDataManager(db)
        # print(data_manager.get_all_users())
        # for user in data_manager.get_all_users():
        #     print(f" {user.username} (ID: {user.user_id})")
        #     print(user.favorite_movies)

        # user_movies = data_manager.get_user_movies(1)
        # print(user_movies)

        # print("\n--- Testing add_user ---")
        # new_user_data = {
        #     "username": "test_new_userone",
        #     "email": "test_new_userone@example.com",
        #     "password_hash": "hashed_password_for_new_userone"
        # }
        # added_user_id = data_manager.add_user(new_user_data)
        # if added_user_id:
        #     print(f"Successfully added user with ID: {added_user_id}")
        # else:
        #     print("Failed to add user.")
        #
        # # Try adding a user with an existing username/email to see error handling
        # print("\n--- Testing add_user (duplicate) ---")
        # duplicate_user_data = {
        #     "username": "test_new_user",  # This should cause an error if unique
        #     "email": "another_email@example.com",
        #     "password_hash": "some_hash"
        # }
        # data_manager.add_user(duplicate_user_data)
        #
        # # Verify the new user is in the database
        # print("\n--- Verifying new user with get_all_users ---")
        # all_users_after_add = data_manager.get_all_users()
        # print("All users after adding:")
        # for user in all_users_after_add:
        #     print(f"- {user.username} (ID: {user.user_id})")

        # print("\n--- Testing add_movie ---")
        # # Ensure you have a user to associate the movie with (e.g., user_id=1)
        # # You might need to add a user first if your DB is empty
        # test_user_id_for_movie = 1  # Replace with an actual user ID from your DB
        #
        # # Example movie data
        # new_movie_data = {
        #     "title": "Dune: Part Two",
        #     "year": 2024,
        #     "rating": 8.8,
        #     "director": "Denis Villeneuve",
        #     "imdb_id": "tt15239678"
        # }
        # added_movie_id = data_manager.add_movie(test_user_id_for_movie, new_movie_data)
        # if added_movie_id:
        #     print(f"Successfully added/associated movie with ID: {added_movie_id}")
        # else:
        #     print("Failed to add/associate movie.")
        #
        # # Test adding an existing movie to the same user (should indicate already a favorite)
        # print("\n--- Testing add_movie (existing movie, same user) ---")
        # data_manager.add_movie(test_user_id_for_movie, new_movie_data)
        #
        # # Test adding an existing movie to a different user (if you have another user)
        # # test_user_id_for_movie_2 = 2 # Replace with another actual user ID
        # # if test_user_id_for_movie_2 != test_user_id_for_movie:
        # #     print("\n--- Testing add_movie (existing movie, different user) ---")
        # #     data_manager.add_movie(test_user_id_for_movie_2, new_movie_data)
        #
        # # Verify the movie is associated with the user
        # print("\n--- Verifying movies for user after adding ---")
        # user_movies_after_add = data_manager.get_user_movies(test_user_id_for_movie)
        # if user_movies_after_add:
        #     print(f"Movies for user ID {test_user_id_for_movie}:")
        #     for movie in user_movies_after_add:
        #         print(f"- {movie.title}")

        # print("\n--- Testing update_movie ---")
        # # Assuming user_id=1 has movie_id=1 (e.g., The Matrix) in their favorites
        # test_user_id_for_update = 1
        # test_movie_id_to_update = 1
        #
        # update_data = {
        #     "rating": 9.0,
        #     "year": 1999  # No change, just for demonstration
        # }
        #
        # # First, print current movie details to see the change
        # print(f"Before update: Movie ID {test_movie_id_to_update} details for user {test_user_id_for_update}:")
        # user_movies_before_update = data_manager.get_user_movies(test_user_id_for_update)
        # for movie in user_movies_before_update:
        #     if movie.movie_id == test_movie_id_to_update:
        #         print(f"  Title: {movie.title}, Year: {movie.year}, Rating: {movie.rating}")
        #         break
        #
        # update_success = data_manager.update_movie(test_user_id_for_update, test_movie_id_to_update, update_data)
        # if update_success:
        #     print(f"Update successful for movie ID {test_movie_id_to_update}.")
        # else:
        #     print(f"Update failed for movie ID {test_movie_id_to_update}.")
        #
        # # Verify the update
        # print(f"\nAfter update: Movie ID {test_movie_id_to_update} details for user {test_user_id_for_update}:")
        # user_movies_after_update = data_manager.get_user_movies(test_user_id_for_update)
        # for movie in user_movies_after_update:
        #     if movie.movie_id == test_movie_id_to_update:
        #         print(f"  Title: {movie.title}, Year: {movie.year}, Rating: {movie.rating}")
        #         break
        #
        # # Test updating a movie not in user's favorites
        # print("\n--- Testing update_movie (movie not in user's favorites) ---")
        # # Assuming user_id=1 does NOT have movie_id=99 in favorites
        # data_manager.update_movie(test_user_id_for_update, 99, {"rating": 10.0})
        #
        # # Test with non-existent user
        # print("\n--- Testing update_movie (non-existent user) ---")
        # data_manager.update_movie(999, test_movie_id_to_update, {"rating": 10.0})

        # print("\n--- Testing delete_movie ---")
        # # Assuming user_id=1 has movie_id=1 (e.g., The Matrix) in their favorites
        # test_user_id_for_delete = 1
        # test_movie_id_to_delete = 1
        #
        # # First, show current movies for the user
        # print(f"Movies for user ID {test_user_id_for_delete} BEFORE deletion:")
        # movies_before_delete = data_manager.get_user_movies(test_user_id_for_delete)
        # for movie in movies_before_delete:
        #     print(f"- {movie.title}")
        #
        # delete_success = data_manager.delete_movie(test_user_id_for_delete, test_movie_id_to_delete)
        # if delete_success:
        #     print(f"Deletion successful for movie ID {test_movie_id_to_delete}.")
        # else:
        #     print(f"Deletion failed for movie ID {test_movie_id_to_delete}.")
        #
        # # Verify the deletion
        # print(f"\nMovies for user ID {test_user_id_for_delete} AFTER deletion:")
        # movies_after_delete = data_manager.get_user_movies(test_user_id_for_delete)
        # if movies_after_delete:
        #     for movie in movies_after_delete:
        #         print(f"- {movie.title}")
        # else:
        #     print("No movies left for this user.")
        #
        # # Test deleting a movie not in user's favorites
        # print("\n--- Testing delete_movie (movie not in user's favorites) ---")
        # # Assuming user_id=1 does NOT have movie_id=99 in favorites
        # data_manager.delete_movie(test_user_id_for_delete, 99)
        #
        # # Test with non-existent user
        # print("\n--- Testing delete_movie (non-existent user) ---")
        # data_manager.delete_movie(999, test_movie_id_to_delete)