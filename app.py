from flask import Flask
from datamanager.json_data_manager import JSONDataManager

# Initialize Flask application
app = Flask(__name__)

data_manager = JSONDataManager('users.json')  # Use the appropriate path to your JSON file
# Test route
@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)  # Temporary users as a string

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
