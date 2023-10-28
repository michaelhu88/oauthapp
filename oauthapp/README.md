# LinkedIn OAuth Flask Application

## Overview
This application demonstrates the usage of LinkedIn's OAuth 2.0 for user authentication in a Flask web application. Users can sign in using their LinkedIn credentials, and the app will retrieve and display the user’s basic profile information.

## Prerequisites
- Python (3.6 or newer)
- Flask
- requests
- requests_oauthlib

## Setup and Installation

### 1. Clone the Repository (Optional)
Clone this repository to your local machine.

```shell
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up Virtual Environment
Create and activate a virtual environment.

For Windows:

```shell
python -m venv env
.\env\Scripts\activate
```

For Unix or MacOS:

```shell
python -m venv env
source env/bin/activate
```

### 3. Install Required Packages

```shell
pip install Flask requests requests_oauthlib
```

### 4. Set Up LinkedIn App
Create a new application through LinkedIn's Developer portal, and obtain your Client ID and Client Secret. Set your application's redirect URI to http://127.0.0.1:5000/auth/linkedin/callback.

Replace YOUR_LINKEDIN_CLIENT_ID and YOUR_LINKEDIN_CLIENT_SECRET in your Python file with your actual LinkedIn app credentials.

### 5. Run the Application

```shell
python linkedin_oauth.py
```

Open a web browser and access http://127.0.0.1:5000/.

## Usage
Users can log in with their LinkedIn credentials. Upon successful authentication, the application will display the user’s first and last name.

## License
This project is licensed under the terms of the MIT license.

## Acknowledgements
Thanks to LinkedIn for providing the OAuth 2.0 authentication mechanism.

## Support
For support or issues, please submit a GitHub issue or contact the repository owner.



