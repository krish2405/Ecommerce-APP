E-Commerce Django Project

This project is a minimal e-commerce backend built with Django, Django REST Framework, MySQL, Redis, and Celery. It supports JWT authentication, product management, cart and order handling, and asynchronous task processing with Celery.

1. Clone the Repository
# Clone the project and navigate into it
git clone https://github.com/krish2405/Project_Alpha.git
cd Project_Alpha

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

The Superuser can only update or create a product ,rest registered user can only buy or see products

