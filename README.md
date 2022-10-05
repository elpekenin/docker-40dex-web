Files used to build [my website](http://elpekenin.tk/40dex)'s docker container. Take also a look at [bot's repo](https://github.com/elpekenin/docker-bot-web)

By no means a complete tutorial here. If you want to make a copy, you'll need to add a `.env` file with your own MongoDB instance credentials, and bot token.... and everything should work. Your `compose.yml` should be similar to:
```
version: "3.9"
services:
  web:
    build: https://raw.githubusercontent.com/elpekenin/docker-website/main/Dockerfile
    container_name: web
    environment:
      DB_IP: "${DB_IP}"
      DB_USER: "${DB_USER}"
      DB_PASS: "${DB_PASS}"
      DB_AUTH: "${DB_AUTH}"
    ports:
      - 80:5000
    restart: always
    volumes:
      - type: bind
        source: ./web/logs
        target: /app/logs

  bot-web:
    build: https://raw.githubusercontent.com/elpekenin/docker-bot-web/main/Dockerfile
    container_name: bot-web
    environment:
      DB_URI: "${DB_URI}" #uri takes precedence over parameterized login

      DB_IP: "${DB_IP}"
      DB_USER: "${DB_USER}"
      DB_PASS: "${DB_PASS}"
      DB_AUTH: "${DB_AUTH}"
      BOT_TOKEN: "${BOT_TOKEN}"
      BOT_USERNAME: "elpekenin" #your telegram username here, without @
    restart: always
    volumes:
      - type: bind
        source: ./bot-web/logs
        target: /app/logs

  mongo:
    image: bitnami/mongodb:latest
    container_name: mongodb
    ports:
      - 27017:27017
    environment:
      MONGODB_ROOT_PASSWORD: "secure-password-here"      
      MONGODB_USERNAME: "${DB_USER}"
      MONGODB_PASSWORD: "${DB_PASS}"
      MONGODB_DATABASE: website
    volumes:
      - ./database/data:/bitnami/mongodb
    restart: always
```

If you want to make changes (eg use a different database)
1. Make your own fork
1. Update your Dockerfile to build from it
1. Change code as wished
