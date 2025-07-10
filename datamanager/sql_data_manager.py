from flask_sqlalchemy import SQLAlchemy
from moviweb_app.datamanager.data_manager_interface import DataManagerInterface
from moviweb_app.appORM import app, db, User, Movie, FavoriteMovies  # Import your User model


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_instance):
        self.db = db_instance

    def get_all_users(self):
        """Return a list of all users."""
        return self.db.session.query(User).all()

    def get_user_movies(self, user_id):
        """Return a list of all movies for a specific user."""
        pass

    def add_user(self, user_data):
        """Add a new user."""
        pass

    def add_movie(self, user_id, movie_data):
        """Add a new movie to a user's list."""
        pass

    def update_movie(self, user_id, movie_id, updated_data):
        """Update an existing movie for a user."""
        pass

    def delete_movie(self, user_id, movie_id):
        """Delete a movie from a user's list."""
        pass


# if __name__ == '__main__':
#     with app.app_context():
#         data_manager = SQLiteDataManager(db)
#
#         all_users = data_manager.get_all_users()
#         print("All users from DB:")
#         for user in all_users:
#             print(f" - {user.username}")


if __name__ == "__main__":
    # When running this file directly, we need to set up the Flask app context
    # and pass the db instance to our data manager.
    with app.app_context():
        # Ensure tables are created if they don't exist (optional, but good for testing)
        #db.create_all()

        data_manager = SQLiteDataManager(db)

        # --- Test get_all_users ---
        print("\n--- Testing get_all_users ---")
        all_users = data_manager.get_all_users()
        if all_users:
            print("All users from DB:")
            for user in all_users:
                print(f"- {user.username} (ID: {user.user_id})")
        else:
            print("No users found. Consider populating data first.")

        # --- Example of adding a dummy user for testing (if no users exist) ---
        if not all_users:
            print("\nAdding a dummy user for testing...")
            new_user_data = {
                "username": "testuser",
                "email": "test@example.com",
                "password_hash": "test_hashed_password"
            }
            # Temporarily add user here for testing, will implement add_user method properly later
            test_user = User(
                username=new_user_data["username"],
                email=new_user_data["email"],
                password_hash=new_user_data["password_hash"]
            )
            db.session.add(test_user)
            db.session.commit()
            print(f"Added user: {test_user.username}")
            all_users = data_manager.get_all_users()
            print("Users after adding:")
            for user in all_users:
                print(f"- {user.username} (ID: {user.user_id})")
