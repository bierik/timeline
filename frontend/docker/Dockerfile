FROM node:18.18.2-alpine3.18 as builder

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN corepack enable

WORKDIR /app

COPY pnpm-lock.yaml package.json ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile


COPY ./assets ./assets
COPY ./components ./components
COPY ./layouts ./layout
COPY ./mixins ./mixins
COPY ./pages ./pages
COPY ./plugins ./plugins
COPY ./store ./store
COPY ./tailwind.config.js .
COPY ./nuxt.config.js .
RUN pnpm run build

FROM nginx:stable-alpine

COPY ./docker/default.conf.template /etc/nginx/templates/default.conf.template
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
