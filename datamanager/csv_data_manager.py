import csv
from moviweb_app.datamanager.data_manager_interface import DataManagerInterface


class CSVDataManager(DataManagerInterface):
    def __init__(self, users_file='users.csv', movies_file='movies.csv'):
        self.users_file = users_file
        self.movies_file = movies_file

    def load_users(self):
        """Load users from the CSV file into a dictionary."""
        users = {}
        try:
            with open(self.users_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    users[row['id']] = row['name']
        except FileNotFoundError:
            pass
        return users

    def save_users(self, users):
        """Save users to CSV file."""
        with open(self.users_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name'])
            writer.writeheader()
            for user_id, name in users.items():
                writer.writerow({'id': user_id, 'name': name})

    def load_movies(self):
        """load movies from the CSV file into a dictionary."""
        movies = {}
        try:
            with open(self.movies_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user_id = row['user_id']
                    movie_id = row['movie_id']
                    movie_data = {
                        "name": row["name"],
                        "director": row["director"],
                        "year": int(row["year"]),
                        "rating": float(row["rating"])
                    }
                    if user_id not in movies:
                        movies[user_id] = {}
                    movies[user_id][movie_id] = movie_data
        except FileNotFoundError:
            pass
        return movies

    def save_movies(self, movies):
        """Save movies to the CSV file."""
        with open(self.movies_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['user_id', 'movie_id', 'name', 'director', 'year', 'rating'])
            writer.writeheader()
            for user_id, user_movies in movies.items():
                for movie_id, movie_data in user_movies.items():
                    writer.writerow(
                        {
                            'user_id': user_id,
                            'movie_id': movie_id,
                            'name': movie_data["name"],
                            'director': movie_data["director"],
                            'year': movie_data["year"],
                            'rating': movie_data["rating"]
                        }
                    )

    def get_all_users(self):
        """Return a list of all user IDs."""
        return list(self.load_users().keys())

    def get_user_movies(self, user_id):
        """Return a list of all movies for a specific user."""
        movies = self.load_movies()
        return movies.get(user_id, {})

    def add_user(self, user_id, user_data):
        """Add a new user to the CSV file."""
        users = self.load_users()
        users[user_id] = user_data["name"]
        self.save_users(users)

    def add_movie(self, user_id, movie_data):
        """Add a new movie for a user."""
        movies = self.load_movies()
        if user_id not in movies:
            movies[user_id] = {}
        movie_id = str(len(movies[user_id]) + 1)    # Generate a unique movie ID
        movies[user_id][movie_id] = movie_data
        self.save_movies(movies)

    def update_movie(self, user_id, movie_id, updated_data):
        """Update a specific movie for a user."""
        movies = self.load_movies()
        if user_id in movies and movies and movie_id in movies[user_id]:
            movies[user_id][movie_id].update(updated_data)
            self.save_movies(movies)

    def delete_movie(self, user_id, movie_id):
        """Delete a specific movie for a user."""
        movies = self.load_movies()
        if user_id in movies and movie_id in movies[user_id]:
            del movies[user_id][movie_id]
            self.save_movies(movies)

