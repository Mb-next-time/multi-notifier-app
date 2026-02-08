#!/bin/bash

file_name=".env"
echo "APP_PORT=8000" > ${file_name}
echo "APP_VERSION=0.1.0" >> ${file_name}
echo "POSTGRES_DB=app" >> ${file_name}
echo "POSTGRES_USER=app" >> ${file_name}
echo "POSTGRES_PASSWORD=app" >> ${file_name}

file_name=".env.api.common"
echo "DEBUG=true" > ${file_name}

file_name=".env.api.database"
echo "DATABASE_USER=app" > ${file_name}
echo "DATABASE_PASSWORD=app" >> ${file_name}
echo "DATABASE_HOST=db" >> ${file_name}
echo "DATABASE_NAME=app" >> ${file_name}
echo "DATABASE_ASYNC_DRIVER=postgresql+asyncpg" >> ${file_name}
echo "DATABASE_SYNC_DRIVER=postgresql+psycopg2" >> ${file_name}
echo "DATABASE_PORT=5432" >> ${file_name}

file_name=".env.api.jwt"
echo "JWT_SECRET_KEY=$(openssl rand -hex 32)" > ${file_name}
echo "JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30" >> ${file_name}
echo "JWT_ALGORITHM=HS256" >> ${file_name}
