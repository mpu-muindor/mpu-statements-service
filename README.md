# Справки, заявления

Сервис по оформлению справок, заявлений и запросов Московского Политеха.

[Сайт](https://statements.6an.ru/), где можно посмотреть Swagger и потыкать работу серсиса самому.

Запуск проекта на локалхосте:

```
cd mpu-statements-service/mpu_statements_service
python -m virtualenv venv
venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

или

```
cd mpu-statements-service
docker-compose build
docker-compose up -d
```
