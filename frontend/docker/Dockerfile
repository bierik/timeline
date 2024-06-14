FROM node:22.2.0-alpine3.19 as builder

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN corepack enable

WORKDIR /app

COPY pnpm-lock.yaml package.json ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile


COPY ./assets ./assets
COPY ./public ./public
COPY ./components ./components
COPY ./layouts ./layout
COPY ./mixins ./mixins
COPY ./pages ./pages
COPY ./plugins ./plugins
COPY ./store ./store
COPY ./lib ./lib
COPY ./tailwind.config.js .
COPY ./nuxt.config.js .
RUN pnpm run generate

FROM nginx:stable-alpine

COPY ./docker/default.conf.template /etc/nginx/templates/default.conf.template
COPY ./docker/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/.output/public /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
