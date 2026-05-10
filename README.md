# VotingSite

![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![Django Version](https://img.shields.io/badge/django-6.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)



<table>
  <tr>
    <td><img width="310" height="150" alt="image" src="https://github.com/user-attachments/assets/7f36c5d3-a8e5-4804-adbb-d0b348156afc" /></td>
    <td><img width="310" height="150" alt="image" src="https://github.com/user-attachments/assets/446c2bbe-e058-40c9-94b0-2a94de6cc7b8" /></td>
    <td><img width="310" height="150" alt="image" src="https://github.com/user-attachments/assets/8d2edb2c-0b03-4b39-a66b-0e93f634103a" /></td>
  </tr>
</table>

A Django-based voting platform designed for creating polls.

## Key Features
- **Polls Management**: Categories, questions, and multiple-choice.
- **Advanced Authentication**: Secure login, registration, and password recovery powered by `django-allauth`.
- **Mandatory Email Verification**: Secure registration flow with HTML email notifications.
- **Social OAuth**: Seamless authentication via Google and GitHub.
- **User System**: Custom user model with vote history and verified profile updates.
- **UI**: Fully custom-styled account pages using SASS/SCSS.

## Tech Stack
- ![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white) **Backend**: Django 6.x
- ![SASS](https://img.shields.io/badge/SASS-hotpink.svg?style=flat&logo=sass&logoColor=white) **Frontend**: SASS, JavaScript
- ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite&logoColor=white) **Database**: SQLite

## Setup & Configuration

### 1. Environment Variables
Create a `.env` file in the root directory:
```ini
SECRET_KEY=your_django_secret_key
RECAPTCHA_PUBLIC_KEY=your_recaptcha_key
RECAPTCHA_PRIVATE_KEY=your_recaptcha_secret
EMAIL_NAME=your_gmail_address
EMAIL_APP_PASSWORD=your_16_digit_app_password
```

### 2. Social OAuth Setup

#### Google Integration
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and navigate to **APIs & Services > Credentials**.
3. Configure the **OAuth Consent Screen** (set User Type to External).
4. Click **Create Credentials > OAuth client ID**.
5. Select **Web application** and add this Authorized Redirect URI:
   `http://<your URL>/accounts/google/login/callback/`
6. Copy the **Client ID** and **Client Secret**.

#### GitHub Integration
1. Go to **Settings > Developer settings > OAuth Apps** on GitHub.
2. Click **New OAuth App**.
3. Set **Homepage URL** to `https://<your URL>`.
4. Set **Authorization callback URL** to:
   `https://<your URL>accounts/github/login/callback/`
5. Click **Register application** and generate a new **Client Secret**.

#### Django Admin Configuration
1. Login to your admin panel (`/admin`).
2. Go to **Social Accounts > Social Applications > Add**.
3. Select the Provider (Google/GitHub).
4. Paste your **Client ID** and **Secret Key**.
5. Well done!

### 3. Running the Project
```bash
# Install dependencies
pip install -r requirements.txt

# Compile SCSS
python manage.py compilescss

# Run migrations
python manage.py migrate

# Load test data (fixtures)
python manage.py loaddata polls/fixtures/questions.json

# Start server
python manage.py runserver
```
