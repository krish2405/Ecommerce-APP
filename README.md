E-Commerce Django Project

This project is a minimal e-commerce backend built with Django, Django REST Framework, MySQL, Redis, and Celery. It supports JWT authentication, product management, cart and order handling, and asynchronous task processing with Celery.

1. Clone the Repository
# Clone the project and navigate into it
git clone https://github.com/krish2405/Ecommerce-APP.git
cd Ecommerce-APP

2. Create .env File
make changes in the .env file according to your db 

3. Build and Start Docker Containers
# Build and start all containers in detached mode
docker compose up --build -d

# Check the status of containers
docker compose ps

# Enter the Django web container
docker compose exec web bash
Install Python Dependencies ,Inside the web container:
pip install -r requirements.txt

4.Migrate Database and Create Superuser
# Make migrations and migrate DB
python manage.py makemigrations
python manage.py migrate

# Create a Django superuser
python manage.py createsuperuser

# Collect static files for admin UI
python manage.py collectstatic --noinput


