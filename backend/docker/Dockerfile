FROM python:3.12.0-alpine3.18 as builder

WORKDIR /app

RUN apk add --no-cache gcc musl-dev postgresql-dev vips-dev mailcap

COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache \
    python -m pip install poetry==1.3.1 && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi \
    && python -m pip install uwsgi

FROM python:3.12.0-alpine3.18

RUN apk add --no-cache postgresql vips

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY core ./core
COPY bin ./bin
COPY settings.py .
COPY urls.py .
COPY wsgi.py .
COPY manage.py .
COPY docker/uwsgi.ini .
COPY docker/entrypoint.sh .

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["uwsgi", "--show-config", "/app/uwsgi.ini"]
