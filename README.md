# ToDo web-app


The project is about goal management. Each user has access to goals that they can create, edit, delete, and comment on. Each goal has its own status, priority, and deadline date. There is also a functionality to control certain features through a Telegram bot, for which verification is provided.

### Used

---

- Python 3.11
- Django 4.2.3
- Django REST Framework 3.14.0
- VK Social Auth
- PostgreSQL
- Docker
- Docker-compose

### Installation

---
### Linux
1. Clone Repository

    ```bash
    git clone https://github.com/Danilu2537/ToDo-web-app.git
    ```
2. Install Docker and Docker-compose

    ```bash
    sudo apt install docker docker-compose
    ```
3. Create file .env and fill it according to the contents of .env.example

    > Create a bot and get a token \
    > https://t.me/BotFather

    > Get Secret keys for VK OAuth \
    > https://vk.com/apps?act=manage

### Usage

---

1. Go to the project folder

    ```bash
    cd ToDo-web-app
    ```

2. Launch docker-compose

    ```bash
    sudo docker-compose up
    ```

3. Go to the address in the browser http://localhost

### Create a Superuser

---

1. Go to the api container

    ```bash
    sudo docker exec -it api bash
    ```

2. Create a Superuser

    ```bash
    python manage.py createsuperuser
    ```

### Documentation

---

API documentation after runnning is available at: \
    http://localhost:8000/schema \
    http://localhost:8000/schema/swagger-ui
