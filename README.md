# Описание
Телеграм-бот для прямого общения с нейросетью ChatGPT    
поддерживает сохранение контекста в PostgreSQL

# Как запустить
Сначала редактируем .env файл,      
после устанавливаем зависимости
```bash
poetry install
```
Опционально запускаем Postgres в docker(создаст папку data, куда будет сохранять данные)
```bash
docker-compose up -d
```
Запускаем бота
```bash
cd src
poetry run python bot.py
```
