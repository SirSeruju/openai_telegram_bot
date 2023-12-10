# Описание
Телеграм-бот для прямого общения с нейросетью ChatGPT    
поддерживает сохранение контекста в PostgreSQL

# Как запустить
Сначала редактируем .env файл

## С помощью Docker-compose

Собираем образ бота
```bash
docker-compose build
```

Запускаем Postgres(создаст папку data, куда будет сохранять данные) и миграции(опционально)
```bash
docker-compose up -d postgres
docker-compose run --entrypoint "poetry run alembic upgrade head" bot
```

Запускаем бота
```bash
docker-compose up -d bot
```


## С помощью Poetry

Устанавливаем зависимости
```bash
poetry install
```
Ставим переменные окружения
```bash
export $(grep -v '^#' .env | xargs)
```
Заходим в папку с кодом
```bash
cd src
```
Выполняем миграции(опционально)
```bash
poetry run alembic upgrade head
```

Запускаем бота
```bash
poetry run python bot.py
```
