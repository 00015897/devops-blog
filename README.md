DevOps Blog Application

 ID 00015897

This project is a Django-based blog application built as a DevOps coursework project. It includes user authentication, CRUD for posts, a relational PostgreSQL database, Docker-based deployment with Nginx and Gunicorn and a GitHub Actions CI/CD pipeline.

Features
User authentication: registration, login, logout
Models: `Category`, `Post`, `Comment` with many-to-one and many-to-many relationships
CRUD: create, update, delete posts (restricted to the author)
Admin panel: configured with inlines and filters
Static files: served by Nginx from shared Docker volume

*Screenshots of the running application are included in the technical report.*

Technologies
Backend: Django 5, Gunicorn
Testing: pytest-django, flake8
Database: PostgreSQL
Web server: Nginx
Containerization: Docker, Docker Compose
CI/CD: GitHub Actions, Docker Hub

 Local Setup (without Docker)
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables (or copy `.env.example` to `.env` and adjust).
4. Apply migrations and create a superuser:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

 Running with Docker (Local)
1. Copy `.env.example` to `.env` and set values.
2. Build and start services:
   ```bash
   docker compose up --build
   ```
3. The application will be available at `http://localhost`.

 Deployment (production server)
The pipeline deploys to your server (e.g. Azure VM or Eskiz) using Docker Compose with three services: **web** (Django/Gunicorn), **PostgreSQL**, and **Nginx**.

- **Server:** Install Docker and Docker Compose. Open firewall ports 22 (SSH), 80 (HTTP), and 443 (HTTPS if using SSL).
- **Compose on server:** The workflow copies `docker-compose.prod.yml` and `nginx/default.conf` to `~/devops-blog/` and creates `.env` from GitHub Secrets, then runs `docker compose pull` and `docker compose up -d`.
- **Migrations** run automatically when the web container starts (entrypoint).
- **Static files** are collected at image build time and served by Nginx.

**GitHub Secrets required:**  
`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `SSH_HOST`, `SSH_USERNAME`, `SSH_PRIVATE_KEY`, `POSTGRES_PASSWORD`, `DJANGO_SECRET_KEY`

**HTTPS (optional):** Use `nginx/default-ssl.conf.example` with Let's Encrypt certs; point a domain to your server and configure SSL.

 Test user (for assessors)
Create on the **live** app (e.g. via Admin or `createsuperuser`):
- Username: `assessor`
- Password: `testpass123`

 Environment variables
See `.env.example`. Production values are set by the CI/CD pipeline from GitHub Secrets (see above). For local or Docker: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, and PostgreSQL variables.
