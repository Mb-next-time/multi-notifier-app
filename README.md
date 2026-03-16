### Описание
Сервис для рассылки уведомлений по расписанию в разные каналы (Email, SMS and etc),  
для первой версии планируется использовать Email провайдер.
### Стек
- FastAPI
- SQLAlchemy(ORM)
- Alembic(Миграции)
- PyTest
- Poetry(Управление зависимостями проекта) 
- Taskiq(Планировщик, фоновые задачи)
- База данных: PostgreSQL
- Брокер: RabbitMQ
- Контейниризация: Docker
### Технические детали
- Чувствительные переменные для сервиса вынесены в environment variables
Пример переменных в файлах env.examaple.*  
- Для PostgreSQL настроен async драйвер
- Покрытие unit тестами Router уровня
- Деления модуля на слои
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