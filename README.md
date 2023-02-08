## Foodgram-project
## Итоговый проект курса Яндекс. Практикум. "Python-разработчик"
Проект размещен здесь: http://51.250.9.68/signup
Данные для входа: электронная почта: 2@mail.ru, пароль: 2
## Описание
Сервис, позволяющий пользователям оставлять свои любимые рецепты, подписываться на публикации понравившихся рецептов, сохранять рецепты и скачивать список продуктов для рецепта.
Сайт доступен по ссылке ......
Тестовый пользователь yuriygrishin


### Запуск проекта

Скопировать репозиторий:

git clone https://github.com/Yuriy-Grishin/foodgram-project-react.git


Cоздаnm и активировать виртуальное окружение:

python3 -m venv env


source venv/bin/activate


Установить зависимости из файла requirements.txt:

python3 -m pip install --upgrade pip


pip install -r requirements.txt


Перейти в директорию проекта:

cd backend


Создайть файл .env в директории backend и заполнить по аналогии:

SECRET_KEY = ваш секретный код DB_ENGINE=django.db.backends.postgresql DB_NAME=postgres POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres DB_HOST=db DB_PORT=5432 DEBUG = True


Создать образ backend из директории backend:

docker build -t ..... .


Перейти в директорию infra:

cd infra


Запустить docker-compose:

docker-compose up


Выполнить миграции в контейнере:

docker-compose exec -T backend python manage.py migrate


Загрузить статику:

docker-compose exec -T backend python manage.py collectstatic --no-input


Запустить проект в браузере.
Ввести в адресную строку браузера http://51.250.9.68/signup


## Стек технологий:
Python
React
Django
Django REST Framework 
Linux
Docker
Docker-compose
Postgres
Gunicorn
Nginx
Workflow
