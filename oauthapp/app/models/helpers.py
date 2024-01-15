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
            title = exp_data.get('title')
        )
        db.session.add(experience)
    
    for edu_data in data.get('education', []):
        education = Education(
            profile = profile,
            timePeriod = json.dumps(edu_data.get('timePeriod')),
            degreeName = edu_data.get('degreeName'),
            schoolName = edu_data.get('schoolName')
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
            timePeriod = json.dumps(edu_data.get('timePeriod')),
            description = proj_data.get('description'),
            title = proj_data.get('title'),
            url = proj_data.get('url')
        )
        db.session.add(projects)
    
    db.session.add(profile)
    db.session.commit()



def compare_data(vanity_name, new_data):
    existing_profile = Profile.query.filter_by(username=vanity_name).first()
    diffs = {
        'profile': {},
        'education': {},
        'experience': {},
        'languages': {},
        'projects': {}
    }

    diffs['profile'].update(compare_table_columns(Profile, existing_profile, new_data))

    existing_educations = Education.query.filter_by(profile_id=existing_profile.id).all()
    new_educations = new_data.get('education', [])  # Assuming this is a list of education records
    for ed in existing_educations:
        diffs['education'] = compare_table_columns(Education, ed, new_educations)

    diffs['education'].update(compare_table_columns(Education, existing_profile, new_data))
    diffs['experience'].update(compare_table_columns(Experience, existing_profile, new_data))
    diffs['languages'].update(compare_table_columns(Languages, existing_profile, new_data))
    diffs['projects'].update(compare_table_columns(Projects, existing_profile, new_data))

    return diffs

def compare_table_columns(table, profile, data):
    table_diffs = {}
    for column in table.__table__.columns:
        column_name = column.key
        current_value = getattr(profile, column_name, None)
        new_value = data.get(column_name)

        if current_value != new_value and new_value is not None:
            table_diffs[column_name] = {'current': current_value, 'new': new_value}

    return table_diffs









