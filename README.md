# Дипломный проект
## Домашняя работа №37

### Описание

---

Проект по работе с целями. Каждому пользователю доступны цели, которые он может создавать, редактировать, удалять,
писать комментарии. Каждая цель имеет свои статус и приоритет, а также дату дедлайна.


### Используется

---

- Python 3.11
- Django 4.2.3
- Django REST Framework 3.14.0
- Авторизация через VK Social Auth
- База данных PostgreSQL
- Docker
- Docker-compose
- Nginx

### Установка

---
### Linux
1. Склонировать репозиторий

    ```bash
    git clone https://github.com/Danilu2537/diplom.git
    ```
2. Установить Docker и Docker-compose

    ```bash
    sudo apt install docker docker-compose
    ```

### Запуск

---

1. Перейти в папку с проектом

    ```bash
    cd diplom
    ```

2. Запустить docker-compose

    ```bash
    sudo docker-compose up
    ```

3. Перейти в браузере по адресу http://localhost

### Добавление суперпользователя

---

1. Перейти в контейнер api

    ```bash
    sudo docker exec -it api bash
    ```

2. Создать суперпользователя

    ```bash
    python manage.py createsuperuser
    ```

### Документация

---

1. ...


>В работе
