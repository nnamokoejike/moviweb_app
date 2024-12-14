import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from datamanager.json_data_manager import JSONDataManager

API_KEY = "778ff5fc"

# Initialize Flask application
app = Flask(__name__)
app.secret_key = "supersecretkey"  # For flask messages

data_manager = JSONDataManager('users.json')  # path to your JSON file


@app.errorhandler(404)
def page_not_found_error(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Home route
@app.route('/')
def home():
    return render_template('home.html')


# Users List route
@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


# User Movies route
@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = data_manager.get_user_by_id(user_id)
    if not user:
        flash(f"No user found with ID {user_id}", "danger")
        return redirect(url_for('list_users'))
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies, user_id=user_id)


# Add User route
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form.get('user_name', '').strip()
        if not user_name:
            flash("User name cannot be empty.", "danger")
            return redirect(url_for('add_user'))

        result = data_manager.add_user({"name": user_name})
        if "successfully" in result:
            flash(result, "success")
            return redirect(url_for('list_users'))
        else:
            flash(result, "danger")
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/delete', methods=['GET'])
def delete_user(user_id):
    """Delete a user and their associated movies."""
    result = data_manager.delete_user(user_id)
    flash(result, "success" if "successfully" in result else "danger")
    return redirect(url_for('list_users'))


def fetch_movie_data_from_api(movie_title):
    """Fetch movie data from OMDb API based on movie title."""
    try:
        response = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_title}")
        response.raise_for_status()  # Raise HTTPError if response code is not 200
        data = response.json()

        if data.get("Response") == "False":
            return None  # Movie not found

        return {
            'name': data.get('Title', movie_title),
            'director': data.get('Director', 'Unknown'),
            'year': int(data.get('Year')) if data.get('Year') and data.get('Year').isdigit() else None,
            'rating': float(data.get('imdbRating')) if data.get('imdbRating') and data.get('imdbRating').replace('.',
                                                                                                                 '',
                                                                                                                 1).isdigit() else None
        }
    except Exception as e:
        print(f"Error fetching movie data: {e}")
        return None


# Add Movie route
@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        movie_title = request.form.get('title')

        if not movie_title:
            flash("Movie title cannot be empty.", "danger")
            return redirect(url_for('add_movie', user_id=user_id))

        movie_data = fetch_movie_data_from_api(movie_title)

        if not movie_data:
            flash(f"Could not fetch data for movie '{movie_title}'. Ensure the title is correct.", "danger")
            return redirect(url_for('add_movie', user_id=user_id))

        result = data_manager.add_movie(user_id, movie_data)
        flash(result, "success" if "successfully" in result else "danger")
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)


# Update Movie route
@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movie = data_manager.get_user_movies(user_id).get(str(movie_id))
    if not movie:
        flash(f"Movie ID {movie_id} not found for User ID {user_id}.", "danger")
        return redirect(url_for('user_movies', user_id=user_id))

    if request.method == 'POST':
        updated_data = {
            'name': request.form['name'],
            'director': request.form['director'],
            'year': request.form['year'],
            'rating': request.form['rating']
        }

        # Call the data manager's update method
        result = data_manager.update_movie(user_id, movie_id, updated_data)
        flash(result, "success" if "successfully" in result else "danger")
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie=movie)


# Delete Movie route
@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    result = data_manager.delete_movie(user_id, movie_id)
    flash(result, "success" if "successfully" in result else "danger")
    return redirect(url_for('user_movies', user_id=user_id))


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
