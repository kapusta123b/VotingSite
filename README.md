# VotingSite

![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
![Django Version](https://img.shields.io/badge/django-6.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

<table>
  <tr>
    <td><img width="310" height="150" alt="image" src="https://github.com/user-attachments/assets/7f36c5d3-a8e5-4804-adbb-d0b348156afc" /></td>
    <td><img width="310" height="150" alt="image" src="https://github.com/user-attachments/assets/446c2bbe-e058-40c9-94b0-2a94de6cc7b8" /></td>
    <td><img width="310" height="150" alt="image" src="https://github.com/user-attachments/assets/8d2edb2c-0b03-4b39-a66b-0e93f634103a" /></td>
  </tr>
</table>

A Django-based voting platform for creating and voting on polls.

## Features

- **Dark Mode Support**: Full support for light and dark themes with a persistent theme switcher.
- **Responsive Design**: Optimized for mobile, tablet, and desktop screens.
- **Real-time Results**: Track poll outcomes with dynamic progress bars.
- **Poll Creation Wizard**: User-friendly multi-step poll creation.
- **User Profiles**: Track created polls and voting history.
- **Category Filtering**: Explore polls by interest (IT, Fun, Politics, etc.).
- **Social Auth**: Login with Google or GitHub.
- **Email Verification**: Secure registration process with styled confirmation emails.

## Tech Stack

- **Backend**: Django 6, Gunicorn
- **Database**: PostgreSQL 16
- **Frontend**: SASS/SCSS, JavaScript
- **Auth**: django-allauth (Social OAuth + Email Verification)
- **Security**: django-recaptcha
- **Server**: nginx
- **Deployment**: Docker + Docker Compose

---

## Local Development

```bash
git clone https://github.com/kapusta123b/VotingSite.git
cd VotingSite

# Setup backend environment
cp backend/.env.example backend/.env # ensure you fill in correct values
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt

# Database setup
python manage.py migrate
python manage.py loaddata fixtures/user/users.json
python manage.py loaddata fixtures/polls/polls_Category.json
python manage.py loaddata fixtures/polls/polls_Question.json
python manage.py loaddata fixtures/polls/polls_Choice.json

# Run server
python manage.py runserver
```

Site available at `http://localhost:8000`

---

## Deployment

### 1. Install Docker on your server

```bash
sudo apt update && sudo apt upgrade -y

sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

sudo usermod -aG docker $USER
newgrp docker
```

### 2. Clone the repository

```bash
git clone https://github.com/kapusta123b/VotingSite.git
cd VotingSite
```

### 3. Configure environment

Fill in `.env` in the root directory and `backend/.env` with real values:

```bash
nano .env
nano backend/.env
```

### 4. Configure nginx

Set your server IP or domain in `conf.d/nginx.conf`:

```nginx
server_name YOUR_SERVER_IP_OR_DOMAIN;
```

### 5. Launch

```bash
docker compose build --no-cache
docker compose up -d
```

Check logs:
```bash
docker compose logs -f web
docker compose logs -f nginx
docker compose logs -f db
```

---

## Social OAuth (Google / GitHub)

Configure after the site is running.

#### Google

1. [Google Cloud Console](https://console.cloud.google.com/) → **APIs & Services → Credentials**
2. Create **OAuth client ID → Web application**
3. Add Authorized Redirect URI: `http://YOUR_DOMAIN/accounts/google/login/callback/`
4. Copy Client ID and Secret

#### GitHub

1. **GitHub → Settings → Developer settings → OAuth Apps → New OAuth App**
2. Homepage URL: `http://YOUR_DOMAIN`
3. Callback URL: `http://YOUR_DOMAIN/accounts/github/login/callback/`
4. Generate Client Secret

#### Add in Django Admin

1. Open `http://YOUR_DOMAIN/admin` → login `creator1` / `Creator1!`
2. **Social Accounts → Social Applications → Add**
3. Add each provider, paste Client ID + Secret, move site to "Chosen sites"

---

## Default credentials

| Login | Password | Role |
|-------|----------|------|
| `creator1` | `Creator1!` | Superuser |
| `test_user1` | `TestUser1!` | Regular user |

Change passwords after first login:
```bash
docker compose exec web python manage.py changepassword creator1
```

---

## Useful commands

```bash
docker compose down              # stop (data preserved)
docker compose down -v           # stop + delete database

docker compose build && docker compose up -d   # rebuild after code changes

docker compose exec web python manage.py shell
docker compose exec db psql -U voting_user -d voting_db
```

---

## Project structure

```
VotingSite/
├── compose.yml
├── requirements.txt
├── .env.example
├── conf.d/
│   └── nginx.conf
└── backend/
    ├── Dockerfile
    ├── entrypoint.sh
    ├── app/
    ├── polls/
    ├── user/
    ├── main/
    ├── templates/       # Global templates (allauth, base)
    ├── static/          # Assets (SCSS, JS, Images)
    ├── media/           # User uploads
    └── fixtures/        # Seed data
```
