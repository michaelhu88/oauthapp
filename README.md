# LinkedIn OAuthApp

## Overview
A Flask application to authenticate and fetch LinkedIn profile data via OAuth. Additional functionalities include an endpoint which detects whether changes have been made to a LinkedIn Profile that has been saved in the database previously. 


## Setup and Installation

### 1. Clone the Repository (Optional)
Clone this repository to your local machine.

```shell
git clone https://github.com/michaelhu88/oauthapp.git
cd oauthapp
```

### 2. Set Up Virtual Environment
Create and activate a virtual environment.

For Windows:

```shell
python -m venv env
env\Scripts\activate
```

For Unix or MacOS:

```shell
python -m venv env
source env/bin/activate
```

### 3. Install Requirements

```shell
pip install -r requirements.txt
```

### 4. Set up your environment variables in a .env file in the root directory, with the following variables:
```
EMAIL=your_email@example.com
PASSWORD=your_password
```

### 5. Run the Application

```shell
python run.py
```

Open a web browser and access http://127.0.0.1:5000/.

## Usage
This application provides endpoints to fetch and compare data from LinkedIn. To use these endpoints, a valid LinkedIn account is required for authentication.

- Endpoint 1: `/fetch` (POST): Fetches data from LinkedIn. Requires authentication via a valid LinkedIn account.
- Endpoint 2: `/compare` (POST): Compares data from LinkedIn. Requires authentication via a valid LinkedIn account.

To authenticate, provide your LinkedIn email and password in the `.env` file as shown in the Setup section.

## License
This project is licensed under the terms of the MIT license.

## Acknowledgements
Special thanks to Tom Quirk for the [linkedin-api](https://github.com/tomquirk/linkedin-api) which this project utilizes to interact with LinkedIn.

## Support
For support or issues, please submit a GitHub issue or contact the repository owner.



