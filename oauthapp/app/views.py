from flask import request, jsonify
from . import app  # Import the Flask app instance
from .models import save_user_data, load_user_data, compare_data  # Import helper functions from models.py
from linkedin_api import Linkedin

email = app.config['EMAIL']
password = app.config['PASSWORD']

@app.route('/fetch', methods=['POST'])
def fetch_data():
    vanity_name = request.json.get('username')
    api = Linkedin(email, password)
    user_info = api.get_profile(vanity_name)
    
    # Remove all occurrences of trackingId from the data
    save_user_data(vanity_name, user_info)
    return jsonify({"message": "Data fetched and saved successfully!"})

@app.route('/compare', methods=['POST'])
def compare():
    vanity_name = request.json.get('username')
    api = Linkedin(email, password)
    new_data = api.get_profile(vanity_name)
    old_data = load_user_data(vanity_name)

    if not old_data:
        return jsonify({"error": "No saved data found for this username!"}), 404
    diffs = compare_data(old_data, new_data)
    return jsonify(diffs)