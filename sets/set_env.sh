#!/bin/sh

# Django
export SECRET_KEY="your_strong_secret_key_here"
export ALLOWED_HOSTS="your-server-ip,your-domain.com"
export CSRF_TRUSTED_ORIGINS="http://your-server-ip,https://your-domain.com"
export DEBUG="False"

# Database
export DB_NAME="voting_db"
export DB_USER="voting_user"
export DB_PASS="strong_random_password_here"
export DB_HOST="db"
export DB_PORT="5432"

# reCAPTCHA
export RECAPTCHA_PUBLIC_KEY="your_recaptcha_public_key"
export RECAPTCHA_PRIVATE_KEY="your_recaptcha_private_key"

# Email
export EMAIL_NAME="your_email@gmail.com"
export EMAIL_APP_PASSWORD="your_16_digit_app_password"
