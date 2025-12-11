## FOODGRAM
Ссылка на сервис: 51.250.67.176/signup
Данные для тестирования возможностей сервиса: электронный адрес: yuyu@mail.ru, пароль: ______

## Возможности сервиса
FOODGRAM представляет собой платформу для людей, которые любят готовить! Данная платформа позволяет: 1. Создать рецепт с указанием ингредиентов (из встроеного списка), времени приготовления, добавить картинку рецепта. 2. Сохранить, отредактировать либо удалить рецепт. 3. Добавить понравившийся рецепт в избранное либо удалить из избраного. 4. Добавить продукты из рецепта в отдельный список и выгрузить его. 5. Подписаться либо отписаться от автора рецепта. И это не все возможности FOODGRAM. Зайди и убедись! 

### Как запустить?

Копируем репозиторий:
git clone https://github.com/Yuriy-Grishin/Foodgram-project-react.git
Cоздаем виртуальное окружение:
python -m venv env
source venv/bin/activate
Устанавливаем зависимость с requirements.txt:
pip install -r requirements.txt
Переходим в папку проектв: cd backend
Создаем файл .env со следующим содержанием:
SECRET_KEY = SECRET_KEY; DB_ENGINE=django.db.backends.postgresql; DB_NAME=postgres POSTGRES_USER=postgres; POSTGRES_PASSWORD=postgres; DB_HOST=db; DB_PORT=5432
Создаем образ: docker build -t yuriygrishin/foodgram-backend:latest .
Перейти в папку infra: cd infra и запускаем команду docker-compose up
Сделай миграции, статику, суперпользователя:
docker-compose exec -T backend python manage.py makemigrations
docker-compose exec -T backend python manage.py migrate
docker-compose exec -T backend python manage.py collectstatic --no-input
docker-compose exec web python manage.py createsuperuser
Введи в браузере: 51.250.67.176/signup

## В работе использовались:
Python
Django
DRF
Docker
Postgres
Nginx
cd 
