# VotingSite

![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
![Django Version](https://img.shields.io/badge/django-6.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-336791.svg)
![Docker](https://img.shields.io/badge/docker-supported-2496ED.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Django-based voting platform for creating, managing, and voting on polls.

The project includes user accounts, poll categories, social authentication, email verification, and Docker-based deployment.

<table>
  <tr>
    <td><img width="310" height="150" alt="VotingSite screenshot" src="https://github.com/user-attachments/assets/7f36c5d3-a8e5-4804-adbb-d0b348156afc" /></td>
    <td><img width="310" height="150" alt="VotingSite screenshot" src="https://github.com/user-attachments/assets/446c2bbe-e058-40c9-94b0-2a94de6cc7b8" /></td>
    <td><img width="310" height="150" alt="VotingSite screenshot" src="https://github.com/user-attachments/assets/8d2edb2c-0b03-4b39-a66b-0e93f634103a" /></td>
  </tr>
</table>

<table>
  <tr>
    <td><img width="310" height="150" alt="image" src="https://github.com/user-attachments/assets/4a6aa182-c788-4e01-a4ec-e89c64683c2b" /></td>
    <td><img width="310" height="150" alt="image" src="https://github.com/user-attachments/assets/c35f8271-b539-445d-bb1d-f7f52e868128" /></td>
    <td><img width="310" height="150" alt="image" src="https://github.com/user-attachments/assets/445996bc-ba9c-4ee1-ad4a-1801b613a4bf" /></td>
  </tr>
</table>

---

## Features

- Poll creation
- Voting system
- Poll categories
- User profiles
- Voting history
- Dark mode
- Responsive layout
- Google and GitHub authentication
- Email verification
- reCAPTCHA protection
- Docker Compose setup

---

## Stack

- Python 3.13
- Django 6.0
- PostgreSQL 16
- Gunicorn
- Nginx
- SASS / SCSS
- JavaScript
- django-allauth
- django-recaptcha
- Docker / Docker Compose

---

## Project Structure

```text
VotingSite
├── backend
│   ├── app
│   ├── polls
│   ├── user
│   ├── main
│   ├── templates
│   ├── static
│   ├── media
│   ├── fixtures
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── manage.py
├── conf.d
│   └── nginx.conf
├── compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## Installation

### Docker

Clone the repository:

```bash
git clone https://github.com/kapusta123b/VotingSite.git
cd VotingSite
```

Create environment files:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
```

Edit environment variables:

```bash
nano .env
nano backend/.env
```

Update Nginx server name:

```bash
nano conf.d/nginx.conf
```

Example:

```nginx
server_name your_server_ip_or_domain;
```

Build and start containers:

```bash
docker compose -f compose.yml up -d --build
```

Apply migrations:

```bash
docker exec votingsite-web-1 python manage.py migrate
```

Load demo data ( not necessarily ):

```bash
docker compose -f compose.yml exec web python manage.py loaddata fixtures/user/users.json
docker compose -f compose.yml exec web python manage.py loaddata fixtures/polls/polls_Category.json
docker compose -f compose.yml exec web python manage.py loaddata fixtures/polls/polls_Question.json
docker compose -f compose.yml exec web python manage.py loaddata fixtures/polls/polls_Choice.json
```

Create admin user:

```bash
docker compose -f compose.yml exec web python manage.py createsuperuser
```

---

### Manual Installation only for DEV

Use this setup for local development.

Clone the repository:

```bash
git clone https://github.com/kapusta123b/VotingSite.git
cd VotingSite
```

Create backend environment file:

```bash
cp backend/.env.example backend/.env
```

Create virtual environment:

```bash
cd backend
python -m venv .venv
```

Activate virtual environment:

Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r ../requirements.txt
```

Apply migrations:

```bash
python manage.py migrate # very important!
```

Load demo data:

```bash
python manage.py loaddata fixtures/user/users.json
python manage.py loaddata fixtures/polls/polls_Category.json
python manage.py loaddata fixtures/polls/polls_Question.json
python manage.py loaddata fixtures/polls/polls_Choice.json
```

Create admin user:

```bash
python manage.py createsuperuser
```

Run development server:

```bash
python manage.py runserver
```

Site is available at:

```text
http://localhost:8000
```

---

## Social Authentication

The project supports Google and GitHub authentication through `django-allauth`.

After deployment, create OAuth applications in Google Cloud Console and GitHub Developer Settings.

Required callback URLs:

```text
http://your_domain/accounts/google/login/callback/
http://your_domain/accounts/github/login/callback/
```

Then add the providers in Django Admin:

```text
Social Accounts -> Social Applications -> Add
```

---

## Default Demo Users

| Login | Password | Role |
|---|---|---|
| `creator1` | `Creator1!` | Superuser |
| `test_user1` | `TestUser1!` | User |

Change default passwords after first login.

```bash
docker exec votingsite-web-1 python manage.py changepassword creator1
```

---

## Useful Commands

Start containers:

```bash
docker compose compose.yml up -d
```

Stop containers:

```bash
docker compose compose.yml down
```

Stop containers and remove volumes:

```bash
docker compose compose.yml down -v
```

Rebuild containers:

```bash
docker compose compose.yml up -d --build
```

View logs:

```bash
docker compose compose.yml logs -f
```

Open Django shell:

```bash
docker exec votingsite-web-1 python manage.py shell
```

Open PostgreSQL shell:

```bash
docker exec votingsite-db-1 psql -U voting_user -d voting_db
```

---

## Notes

Before deployment, update:

- `.env`
- `backend/.env`
- Nginx `server_name`
- OAuth credentials
- default demo user passwords

Do not commit real secrets or production credentials to the repository.

---

## License

MIT
