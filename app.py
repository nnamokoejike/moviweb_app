import requests
from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager

API_KEY = "778ff5fc"

# Initialize Flask application
app = Flask(__name__)

data_manager = JSONDataManager('users.json')  # Use the appropriate path to your JSON file


@app.errorhandler(404)
def page_not_found_error(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Home route (placeholder)
@app.route('/')
def home():
    return render_template('home.html')


# Users List route
@app.route('/users')
def list_users():
    users = data_manager.get_all_users()  # Fetch all users
    return render_template('users.html', users=users)  # Pass users to the template


# Placeholder for the user_movies route
@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = data_manager.get_user_by_id(user_id)  # Fetch user data, including the name
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


# Add User to the route
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # user_id = request.form['user_id']
        user_name = request.form['user_name']
        data_manager.add_user(user_name)
        # data_manager.add_user(user_id, {'name': user_name})
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


def fetch_movie_data_from_api(movie_title):
    try:
        response = requests.get(f'http://www.omdbapi.com/?i=tt3896198&apikey={API_KEY}&t={movie_title}')
        response.raise_for_status()  # Raise HTTPError if response code is not 200
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to OMDb API: {e}")
        return render_template('error.html', message="Could not connect to OMDb API. Please try again later.")
    except ValueError as e:
        print(f"Error: {e}")
        return render_template('error.html', message="Movie not found. Please enter a valid title")


# Add movie to the route
@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        movie_title = request.form['title']
        movie_data = fetch_movie_data_from_api(movie_title)

        if movie_data:
            movie_details = {
                'name': movie_data.get('Title', movie_title),
                'director': movie_data.get('Director', 'Unknown'),
                'year': movie_data.get('Year', 'N/A'),
                'rating': movie_data.get('imdbRating', 'N/A')
            }
            # Add movie to user's list
            data_manager.add_movie(user_id, movie_details)
            return redirect(url_for('user_movies', user_id=user_id))
        else:
            return render_template('error.html', message='Sorry we could not fetch the movie data.')
    return render_template('add_movie.html', user_id=user_id)


# Update the route
@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movie = data_manager.get_user_movies(user_id).get(movie_id)
    if request.method == 'POST':
        updated_data = {
            'name': request.form['name'],
            'director': request.form['director'],
            'year': request.form['year'],
            'rating': request.form['rating']
        }
        data_manager.update_movie(user_id, movie_id, updated_data)
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie=movie)


# Delete movie from route
@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
