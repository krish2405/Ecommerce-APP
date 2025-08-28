E-Commerce Django Project

This project is a minimal e-commerce backend built with Django, Django REST Framework, MySQL, Redis, and Celery. It supports JWT authentication, product management, cart and order handling, and asynchronous task processing with Celery.

1. Clone the Repository
# Clone the project and navigate into it project folder


2. Create .env File
### Environment Variables

Copy `example.env` to `.env`
   ```bash
   cp 'example.env' .env
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

#The Superuser can only update or create a product ,rest registered user can only buy or see products



Here is the link for the collection of api and urls used in project:
https://web.postman.co/workspace/My-Workspace~be73eb3d-406a-4238-8417-416b885fa3a2/collection/25232433-eb393265-d59f-4023-b917-8f932b1a1753?action=share&source=copy-link&creator=25232433