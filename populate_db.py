from appORM import app, db, User, Movie, FavoriteMovies


def populate_dummy_data():
    with app.app_context():
        # Clear existing data to prevent duplicates on re-runs (optional, but good for testing)
        db.session.query(FavoriteMovies).delete()
        db.session.query(User).delete()
        db.session.query(Movie).delete()
        db.session.commit()

        # Create dummy users
        user1 = User(username='alice', email='alice@example.com', password_hash='hashed_password_alice')
        user2 = User(username='bob', email='bob@example.com', password_hash='hashed_password_bob')
        user3 = User(username='charlie', email='charlie@example.com', password_hash='hashed_password_charlie')
        user4 = User(username='vincent', email='vincent@example.com', password_hash='hashed_password_vincent')

        db.session.add_all([user1, user2, user3, user4])
        db.session.commit()

        # Create dummy movies
        movie1 = Movie(title='The Matrix', year=1999, rating=8.7, director='The Wachowskis', imdb_id='tt0133093')
        movie2 = Movie(title='Interstellar', year=2014, rating=8.6, director='Christopher Nolan', imdb_id='tt0816692')
        movie3 = Movie(title='Parasite', year=2019, rating=8.5, director='Bong Joon-ho', imdb_id='tt6710474')
        movie4 = Movie(title='Spirited Away', year=2001, rating=8.6, director='Hayao Miyazaki', imdb_id='tt0245429')

        db.session.add_all([movie1, movie2, movie3, movie4])
        db.session.commit()  # commit to get IDs for relationships

        # Create favorite movie associations
        # Alice likes The Matrix and Interstellar
        user1.favorite_movies.append(movie1)
        user1.favorite_movies.append(movie2)

        # Bob likes parasite
        user2.favorite_movies.append(movie3)

        # Chalie likes The Matrix and Spirited Away
        user3.favorite_movies.append(movie1)
        user3.favorite_movies.append(movie4)

        db.session.commit()
        print("Database populate with dummy data!")


if __name__ == '__main__':
    populate_dummy_data()
