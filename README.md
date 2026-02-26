### Описание
Сервис для создания напоминаний, который будет оповещать пользователя  
по разным каналам (Email, SMS and etc), для первой версии планируется 
использовать Email провайдер.  
Для отправки уведомлений и гарантий доставки планируется использовать Celery или Taskiq.
### Стек
- FastAPI, Pydantic(Validation)
- SQLAlchemy(ORM)
- Alembic(Миграции)
- PyTest
- Poetry(Управление зависимостями проекта)  
- База данных: PostgreSQL  
- Контейниризация: Docker
### Технические детали
- Чувствительные переменные для сервиса вынесены в enviroment variables  
Пример переменных в файлах env.examaple.*  
- Для PostgreSQL настроен async драйвер
- Покрытие тестами Router уровня
- Каждый модуль разделен на слои
### Функционал
- Регистрация пользователей
- Логин пользователя (Авторизация через JWT)
- CRUD операции для уведомлений
### Локальный запуск
- Installing (main + dev dependencies)  
`poetry install`  
- Create env files  
`./create_env_files.sh`
- Activating virtual environment  
`$(poetry env activate)`
- Apply Migrations  
`alembic -c src/alembic.ini upgrade head`  
- Run tests  
`pytest`  
- Local start via FastAPI  
`fastapi dev src/main.py`
### Запуск через Docker
- Build and start docker containers  
`docker compose up -d`
### API Documentation URLs
- /redoc  
- /docs