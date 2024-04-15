import os
import json
from .. import db
from .profile import Profile
from .experience import Experience
from .education import Education
from .languages import Languages
from .projects import Projects

DATA_DIR = "linkedin_data"


def save_user_data(vanity_name, data):
    profile = Profile(
    username = vanity_name,
    summary = data.get('summary'),
    industryName = data.get('industryName'),
    lastName = data.get('lastName'),
    locationName = data.get('locationName'),
    geoCountryName = data.get('geoCountryName'),
    geoLocationName = data.get('geoLocationName'),
    headline = data.get('headline'),
    displayPictureUrl = data.get('displayPictureUrl'),
    public_id = data.get('public_id'),
    firstName=data.get('firstName'), )


    for exp_data in data.get('experience', []):
        experience = Experience(
            profile=profile,  # Associate with the profile instance
            companyName=exp_data.get('companyName'),
            #this needs to be serialized
            timePeriod = json.dumps(exp_data.get('timePeriod')),
            description = exp_data.get('description'),
            company = json.dumps(exp_data.get('company')),
            title = exp_data.get('title'),
            entityUrn = exp_data.get('entityUrn')
        )
        db.session.add(experience)
    
    for edu_data in data.get('education', []):
        education = Education(
            profile = profile,
            timePeriod = json.dumps(edu_data.get('timePeriod')),
            degreeName = edu_data.get('degreeName'),
            schoolName = edu_data.get('schoolName'),
            entityUrn = edu_data.get('entityUrn')
        )
        db.session.add(education)

    for lan_data in data.get('languages',[]):
        languages = Languages(
            profile = profile,
            name = lan_data.get('name'),
            proficiency = lan_data.get('proficiency')
        )
        db.session.add(languages)
    
    for proj_data in data.get('projects',[]):
        projects = Projects(
            profile = profile,
            timePeriod = json.dumps(proj_data.get('timePeriod')),
            description = proj_data.get('description'),
            title = proj_data.get('title'),
            url = proj_data.get('url'),
            entityUrn = proj_data.get('entityUrn'),
        )
        db.session.add(projects)
    
    db.session.add(profile)
    db.session.commit()

def compare_table_columns(table, instance, data):
    table_diffs = {}
    for column in table.__table__.columns:
        column_name = column.key
        print(column_name)
        old_value = getattr(instance, column_name, None)
        new_value = data.get(column_name)

        if old_value != new_value and new_value is not None:
            table_diffs[column_name] = {'current': old_value, 'new': new_value}

    return table_diffs

def compare_data(vanity_name, new_data):
    existing_profile = Profile.query.filter_by(username=vanity_name).first()
    if not existing_profile:
        return None 

    diffs = {
        'profile': {},
        'education': [],
        'experience': [],
        'languages': [],
        'projects': []
    }

    diffs['profile'].update(compare_table_columns(Profile, existing_profile, new_data))


    # Function to compare each entry in a list with a corresponding existing entry
    # existing_entries is a list of all rows with profile_id matches
    # new_entries is a list of dictionaries. there are nested dictionaries within the dictionary
    def compare_child_entries(child_table, existing_entries, new_entries):
        child_diffs = []
        if child_table == Languages:
            for new in new_entries: #dictionaries of an education instance
                name = new['name']
                for saved in existing_entries:
                    if name == saved.name:
                        break
                else:
                    child_diffs.append(new)
        elif child_table == Projects:
            for new in new_entries: #dictionaries of an education instance
                name = new['title']
                for saved in existing_entries:
                    if name == saved.title:
                        break
                else:
                    child_diffs.append(new)
        else:
            for new in new_entries: #dictionaries of an education instance
                new_entity = new['entityUrn']
                for saved in existing_entries:
                    if new_entity == saved.entityUrn:
                        break
                else:
                    child_diffs.append(new)
        
        return child_diffs

    diffs['education'] = compare_child_entries(Education, Education.query.filter_by(profile_id=existing_profile.id).all(), new_data.get('education', []))
    diffs['experience'] = compare_child_entries(Experience, Experience.query.filter_by(profile_id=existing_profile.id).all(), new_data.get('experience', []))
    diffs['languages'] = compare_child_entries(Languages, Languages.query.filter_by(profile_id=existing_profile.id).all(), new_data.get('languages', []))
    diffs['projects'] = compare_child_entries(Projects, Projects.query.filter_by(profile_id=existing_profile.id).all(), new_data.get('projects', []))
    return diffs









