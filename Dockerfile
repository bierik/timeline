FROM node:18.18.2-alpine3.18 as frontend-builder

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN corepack enable

WORKDIR /app

COPY frontend/pnpm-lock.yaml frontend/package.json ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm install vue-template-compiler

COPY frontend .

RUN pnpm run build

FROM python:3.12.0-alpine3.18 as builder

WORKDIR /app

RUN apk add --no-cache gcc musl-dev postgresql-dev vips-dev

COPY backend/requirements.txt .

RUN --mount=type=cache,target=/root/.cache \
    python -m pip install -r requirements.txt

RUN python -m pip install uwsgi

FROM python:3.12.0-alpine3.18

RUN apk add --no-cache postgresql vips

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=frontend-builder /tmp/nuxt_output ./staticfiles
COPY backend/core ./core
COPY backend/settings.py .
COPY backend/urls.py .
COPY backend/wsgi.py .
COPY backend/manage.py .
COPY backend/docker/uwsgi.ini .
COPY entrypoint.sh .

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["uwsgi", "--show-config", "/app/uwsgi.ini"]
