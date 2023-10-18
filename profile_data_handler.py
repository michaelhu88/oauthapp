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

    if isinstance(old_data, list) and isinstance(new_data, list):
        differences = []
        for old_item, new_item in zip(old_data, new_data):
            item_diff = compare_data(old_item, new_item)
            if item_diff:
                differences.append(item_diff)
        return differences

    differences = {}
    for key, value in new_data.items():
        if key in IGNORE_KEYS:
            continue
        if key not in old_data:
            differences[key] = value
        else:
            if isinstance(value, dict) or isinstance(value, list):
                nested_diff = compare_data(old_data[key], value)
                if nested_diff:  # Only add to differences if there's a nested difference
                    differences[key] = nested_diff
            elif old_data[key] != value:
                differences[key] = value
    return differences

@app.route('/fetch', methods=['POST'])
def fetch_data():
    vanity_name = request.json.get('username')
    api = Linkedin(email, password)
    user_info = api.get_profile(vanity_name)
    
    # Remove all occurrences of trackingId from the data
    cleaned_data = remove_tracking_id(user_info)
    
    save_user_data(vanity_name, cleaned_data)
    return jsonify({"message": "Data fetched and saved successfully!"})

@app.route('/compare', methods=['POST'])
def compare():
    vanity_name = request.json.get('username')
    api = Linkedin(email, password)
    new_data = api.get_profile(vanity_name)
        
    pretty_json = json.dumps(new_data, indent=4)
    print(pretty_json)
    
    old_data = load_user_data(vanity_name)
    if not old_data:
        return jsonify({"error": "No saved data found for this username!"}), 404
    diffs = compare_data(old_data, new_data)
    save_user_data(vanity_name, new_data)
    return jsonify(diffs)

if __name__ == '__main__':
    app.run(debug=True)