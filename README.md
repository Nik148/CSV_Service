## Описание
HTTP сервис для работы с импортируемыми данными в формате csv. 

Функционал:

Индетификация и аутентификация

Загрузка и удаление файлов пользователя

Получение списка файлов с информацией о них

Получение данных из конкретного файла с возможностями выбора опеределенных столбцов, фильтраций и сортировок

## Инструкция к запуску сервиса
Запуск в локальной системе:

Нужно сначала создать файл .env и в нем прописать ваши парамертры (тестовую бд можно не создавать, она создастся сама при тестировании):
```
DB_URL=postgresql+asyncpg://postgres:admin@localhost:5432/csv_service
TEST_DB_URL=postgresql+asyncpg://postgres:admin@localhost:5432/test_csv_service
TEST_DB_NAME=test_csv_service
```
Подготовка к запуску:
```
python virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```
Запуск сервиса:
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
Docker:
```
docker-compose build
docker-compose up
```
### После запуска сервиса документацию можно посмотреть по url /docs
## Тестирование
```
pytest test
```
