import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from linkedin_api import Linkedin

load_dotenv()

app = Flask(__name__)

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
DATA_DIR = "linkedin_data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def save_user_data(vanity_name, data):
    with open(os.path.join(DATA_DIR, f"{vanity_name}.json"), 'w') as f:
        json.dump(data, f)

def load_user_data(vanity_name):
    filepath = os.path.join(DATA_DIR, f"{vanity_name}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def compare_data(old_data, new_data):
    IGNORE_KEYS = {"expiresAt", "fileIdentifyingUrlPathSegment", "trackingId"}

    # If both old and new data are lists
    if isinstance(old_data, list) and isinstance(new_data, list):
        differences = []
        for old_item, new_item in zip(old_data, new_data):
            item_diff = compare_data(old_item, new_item)
            if item_diff:
                differences.append(item_diff)
        # Handle case where lists are of different lengths
        if len(old_data) > len(new_data):
            differences.extend(old_data[len(new_data):])
        elif len(new_data) > len(old_data):
            differences.extend(new_data[len(old_data):])
        return differences if differences else None

    # If both old and new data are dictionaries
    elif isinstance(old_data, dict) and isinstance(new_data, dict):
        differences = {}
        all_keys = set(old_data.keys()) | set(new_data.keys())
        for key in all_keys:
            if key in IGNORE_KEYS:
                continue
            old_value = old_data.get(key)
            new_value = new_data.get(key)
            if old_value != new_value:
                if isinstance(old_value, (dict, list)) and isinstance(new_value, (dict, list)):
                    nested_diff = compare_data(old_value, new_value)
                    if nested_diff:
                        differences[key] = nested_diff
                else:
                    differences[key] = new_value
        return differences if differences else None

    # If old and new data are of different types or primitive values
    else:
        return None if old_data == new_data else new_data

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

if __name__ == '__main__':
    app.run(debug=True)