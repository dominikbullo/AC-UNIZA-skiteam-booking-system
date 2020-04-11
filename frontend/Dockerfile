FROM node:lts-alpine
LABEL maintainer="dominobullo@gmail.com"

RUN mkdir /app
WORKDIR /app

COPY ./frontend/ /
EXPOSE 8000
EXPOSE 8080


RUN npm install -g npm
RUN npm install -g @vue/cli @vue/cli-service @vue/cli-plugin-babel @vue/cli-plugin-eslint @vue/cli-plugin-pwa

