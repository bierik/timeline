FROM node:22.2.0-alpine3.20 AS builder
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app
COPY pnpm-lock.yaml package.json /app/
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile


FROM builder AS dev
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000
EXPOSE 3000
CMD [ "pnpm", "run", "dev" ]

FROM builder AS prod-builder
COPY . /app/
RUN pnpm run generate-pwa-assets
RUN pnpm run generate

FROM nginx:stable-alpine AS prod
COPY --from=prod-builder /app/.output/public /usr/share/nginx/html
COPY ./docker/default.conf.template /etc/nginx/templates/default.conf.template
COPY ./docker/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
