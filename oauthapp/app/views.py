from flask import request, jsonify
from . import app  # Import the Flask app instance
from .models.helpers import save_user_data, compare_data  # Import helper functions from models.py
from linkedin_api import Linkedin
from .models.profile import Profile
from . import db

email = app.config['EMAIL']
password = app.config['PASSWORD']

@app.route('/fetch', methods=['POST'])
def fetch_data():
    vanity_name = request.json.get('username')
    api = Linkedin(email, password)
    user_info = api.get_profile(vanity_name)
    print(user_info)
    existing_profile = Profile.query.filter_by(username=vanity_name).first()
    if existing_profile:
        db.session.delete(existing_profile)
        db.session.commit()  
    save_user_data(vanity_name, user_info)
    return jsonify({"message": "Data fetched and saved successfully!"})

@app.route('/compare', methods=['POST'])
def compare():
    vanity_name = request.json.get('username')
    api = Linkedin(email, password)
    new_data = api.get_profile(vanity_name)
    existing_profile = Profile.query.filter_by(username=vanity_name).first()
    print(existing_profile)
    if existing_profile == None:
        save_user_data(vanity_name, new_data)
        return jsonify({"message": f"{vanity_name} has not been saved in our records. We have now saved the info."})
    else:
        diffs = compare_data(vanity_name, new_data)
        #save_user_data(vanity_name, new_data)
        return diffs
    
        

    
    