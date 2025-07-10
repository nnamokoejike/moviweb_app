from appORM import app, db, User, Movie, FavoriteMovies


def query_database():
    with app.app_context():
        print("\n ---Verification ---")
        print("All Users:")
        print(User.query.all())
        for user in User.query.all():
            print(f" {user.username} (ID: {user.user_id})")
            # for movie in user.favorite_movies:
            #     print(f"    -{movie.title}")
            #
            # print("\nAll Movies:")
            # for movie in Movie.query.all():
            #     print(f"  {movie.title} (ID: {movie.movie_id})")
            #     for user in movie.users:
            #         print(f"   -Liked by: {user.username}")


if __name__ == '__main__':
    query_database()
