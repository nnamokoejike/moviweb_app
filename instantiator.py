from datamanager.json_data_manager import JSONDataManager

data_manager = JSONDataManager('users.json')

# Adding a user
# data_manager.add_user(user_id=1, name="Omengboji")

# Adding a movie
# data_manager.add_movie(user_id=1, movie_data={
#     "name": "Iheanacho",
#     "director": "Nwachukwu",
#     "year": 2016,
#     "rating": 8.9
# })

# Listing all users
# users = data_manager.get_all_users()
# print(users)

# try:
#     user = data_manager.get_user_by_id(9)
#     print(user)
# except Exception as e:
#     print(f"Caught Exception: {e}")

# Fetching movies for a user
# try:
#     movies = data_manager.get_user_movies(2)
#     print(movies)
# except Exception as e:
#     print(f"Caught NameError: {e}")

# try:
#     user = {"name": "Daniel"}
#     result = data_manager.add_user(user)
#     print(f"Result: {result}")
# except Exception as e:
#     print(f"Caught NameError: {e}")

# try:
#     movie = {'name': 'Inception7', 'director': 'Christopher Nolan7', 'year': 2024, 'rating': 9.6}
#     result = data_manager.add_movie(user_id=3, movie_data=movie)
#     print(f"Result: {result}")
# except Exception as e:
#     print(f"Caught NameError: {e}")

# try:
#     movie = {'name': 'Inception7', 'director': 'Christopher Nolan7', 'year': 2024, 'rating': 9.5}
#     result = data_manager.update_movie(user_id=7, movie_id=1, updated_data=movie)
#     print(f"Result: {result}")
# except Exception as e:
#     print(f"Caught NameError: {e}")

# try:
#     movie = {'name': 'Inception7', 'director': 'Christopher Nolan7', 'year': 2024, 'rating': 9.5}
#     result = data_manager.delete_movie(user_id=3, movie_id=2)
#     print(f"Result: {result}")
# except Exception as e:
#     print(f"Caught NameError: {e}")


# try:
#     result = data_manager.delete_user(user_id=7.5)
#     print(f"Result: {result}")
# except Exception as e:
#     print(f"Caught Exception: {e}")
