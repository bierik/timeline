FROM python:3.12.7-alpine3.20 AS poetry
WORKDIR /app
RUN --mount=type=cache,id=poetry-pip,target=/root/.cache \
    python -m pip install --no-cache-dir \
        poetry==1.8.4 \
        poetry-plugin-export==1.8.0
COPY poetry.lock pyproject.toml /app/
RUN --mount=type=cache,id=poetry,target=/root/.cache \
    poetry lock && \
    poetry export -o requirements.txt --without-hashes && \
    poetry export -o requirements-dev.txt --only dev && \
    poetry export -o requirements-test.txt --only test && \
    poetry export -o requirements-prod.txt --only prod


FROM python:3.12.7-alpine3.20 AS build
WORKDIR /app
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    vips-dev \
    git
COPY --from=poetry /app/requirements.txt /app/requirements/
RUN --mount=type=cache,id=build-pip,target=/root/.cache \
    pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r /app/requirements/requirements.txt && \
    rm -rf /app/requirements
ENV PYTHONUNBUFFERED=1


FROM build AS build-prod
WORKDIR /app
COPY --from=poetry /app/requirements-prod.txt /app/requirements/
RUN --mount=type=cache,id=build-prod-pip,target=/root/.cache \
    pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r /app/requirements/requirements-prod.txt && \
    rm -rf /app/requirements


FROM build AS build-dev
COPY --from=poetry /app/requirements-dev.txt /app/requirements/
RUN --mount=type=cache,id=build-dev-pip,target=/root/.cache \
    pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir \
    -r /app/requirements/requirements-dev.txt && \
    rm -rf /app/requirements


FROM build AS build-test
COPY --from=poetry /app/requirements-test.txt /app/requirements/
RUN --mount=type=cache,id=build-test-pip,target=/root/.cache \
    pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir \
    -r /app/requirements/requirements-test.txt && \
    rm -rf /app/requirements


FROM python:3.12.7-alpine3.20 AS runner
RUN addgroup --system app && adduser --system --ingroup app app
WORKDIR /app
RUN apk add --no-cache \
    postgresql \
    vips
EXPOSE 8000


FROM runner AS dev
COPY --from=build-dev /app /app
COPY --from=build-dev /usr/local/bin /usr/local/bin
COPY --from=build-dev /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
USER app
ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM runner AS prod
COPY --from=build-prod /app /app
COPY --from=build-prod /usr/local/bin /usr/local/bin
COPY --from=build-prod /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . /app/
RUN chown -R app /app/tus
RUN chgrp -R app /app/tus
RUN python manage.py collectstatic --noinput
USER app
ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["uwsgi", "--show-config", "/app/docker/uwsgi.ini"]


FROM runner AS test
COPY --from=build-test /app /app
COPY --from=build-test /usr/local/bin /usr/local/bin
COPY --from=build-test /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . /app/
USER app
CMD ["pytest"]
