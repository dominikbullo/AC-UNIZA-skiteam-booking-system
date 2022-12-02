# Stage 1 - build frontend app
FROM node:18-alpine as build-deps

WORKDIR /app/

COPY frontend/package.json frontend/yarn.lock /app/
RUN yarn

COPY frontend /app/
COPY .env /app/.env
RUN yarn build

# Stage 2 - nginx & frontend dist
FROM nginx:alpine

COPY nginx/prod.conf /etc/nginx/nginx.conf
COPY --from=build-deps /app/dist/ /dist/

CMD ["nginx", "-g", "daemon off;"]
