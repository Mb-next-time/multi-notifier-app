### Description
Application for creating notifications and alerting notifications by time through different channels.  
First version will work with email notifications. 

### Installing
`poetry install`
### Note: Please activate your virtual environment before run commands
`$(poetry env activate)`
### Apply Migrations
`alembic upgrade head`
### Run tests
`pytest`
### Local start
`fastapi dev src/main.py`