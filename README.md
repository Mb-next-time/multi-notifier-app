### Description
Application for creating notifications and alerting notifications by time through different channels.  
First version will work with email notifications. 

### Installing (main + dev dependencies)
`poetry install`
### Note: Please activate your virtual environment before run commands
`$(poetry env activate)`
### Apply Migrations
`alembic upgrade head`
### Run tests
`pytest`
### Local start
`fastapi dev src/main.py`
### Create env files
`./create_env_files.sh`
### Build and start docker containers
`docker compose up -d`