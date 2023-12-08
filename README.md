# Описание
Телеграм-бот для прямого общения с нейросетью ChatGPT    
поддерживает сохранение контекста в PostgreSQL

# Как запустить
Сначала редактируем .env файл

## С помощью Docker-compose
Запускаем Postgres(создаст папку data, куда будет сохранять данные) и бота в docker'е
```bash
docker-compose up -d
```

## С помощью Poetry
Запускаем бота
```bash
poetry install
cd src
poetry run python bot.py
```
