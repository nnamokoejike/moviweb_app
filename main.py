from moviweb_app.datamanager.json_data_manager import JSONDataManager

# Assuming users.json exists with some user data

manager = JSONDataManager()

# Test get_all_users
all_users = manager.get_all_users()
print("All Users:", all_users)

# Test get_user_movies
user_movies = manager.get_user_movies("1")
print("User Movies", user_movies)
