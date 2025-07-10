from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moviweb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # To suppress a warning
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user' # Explicitly define table name for clarity
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Define the many-to-many relationship with movies
    favorite_movies = db.relationship(
        'Movie', secondary='favorite_movies', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.username}>'


class Movie(db.Model):
    __tablename__ = 'movie' # Explicitly define table name for clarity
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    director = db.Column(db.String(120), nullable=False)
    imdb_id = db.Column(db.String(20), unique=True, nullable=True)  # Optional, but good for

    def __repr__(self):
        return f'<Movie {self.title}>'

# Association table for the many-to-many relationship
# This table doesn't need its own model class if it only contains foreign keys
# and doesn't have extra attributes. SQLAlchemy can handle it implicitly.
# However, since we are defining both ORM and raw SQL, lets define it explicitly
# for clarity and easier raw SQL interaction


class FavoriteMovies(db.Model):
    __tablename__ = 'favorite_movies'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True) # Corrected foreign key reference
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True) # Corrected foreign key reference

    def __repr__(self):
        return f'<FavoriteMovies User: {self.user_id}, Movie: {self.movie_id}>'


# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#         print("Database table created!")
