FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    pipx \
    && rm -rf /var/lib/apt/lists/* \
    && pipx ensurepath \
    && pipx install poetry==2.2.1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="/root/.local/bin:$PATH"

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry install --no-cache --no-interaction --no-root --only main

COPY ./src /app/src

FROM python:3.12-slim AS final

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=builder /app/ /app/


ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN rm $VIRTUAL_ENV/bin/pip* /usr/local/bin/pip*
RUN addgroup appgroup && adduser appuser && adduser appuser appgroup
USER appuser
WORKDIR ./src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]