## DevOps Blog Application

This project is a Django-based blog application built as a DevOps coursework project. It includes user authentication, CRUD for posts, a relational PostgreSQL database, Docker-based deployment with Nginx and Gunicorn, and a GitHub Actions CI/CD pipeline.

### Features
- **User authentication**: registration, login, logout
- **Models**: `Category`, `Post`, `Comment` with many-to-one and many-to-many relationships
- **CRUD**: create, update, delete posts (restricted to the author)
- **Admin panel**: configured with inlines and filters
- **Static files**: served by Nginx from shared Docker volume

### Technologies
- **Backend**: Django 5, Gunicorn
- **Database**: PostgreSQL
- **Web server**: Nginx
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions, Docker Hub

### Local Setup (without Docker)
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

### Running with Docker (Local)
1. Copy `.env.example` to `.env` and set values.
2. Build and start services:
   ```bash
   docker compose up --build
   ```
3. The application will be available at `http://localhost`.

### Deployment Overview
- **Server path**: `/srv/devops_blog` on the Eskiz VM
- **Compose file**: `docker-compose.yml` used both locally and in production
- **Static/media**: shared volumes between Django and Nginx containers
- **CI/CD**: pushing to `main` triggers the GitHub Actions workflow:
  - Flake8 lint checks
  - Pytest tests
  - Docker image build and push to Docker Hub
  - SSH to server and `docker compose up -d` + migrations + `collectstatic`

### Environment Variables
See `.env.example` for all required variables:
- **Django**: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`
- **Database**: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`

