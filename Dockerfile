# -- Base --
FROM python:3.11 AS base
LABEL maintainer="Pablo (elpekenin) Martinez Bernal"
LABEL email="martinezbernalpablo@gmail.com"
SHELL ["/bin/bash", "-c"]
WORKDIR /app

# -- Dependencies --
FROM base AS dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# -- Release --
FROM python:3.11-alpine AS release
WORKDIR /app
COPY . .
COPY --from=dependencies /app/requirements.txt .
COPY --from=dependencies /root/.cache /root/.cache

RUN pip3 install -r requirements.txt

ARG DB_URI
ENV DB_URI=$DB_URI

ARG GH_LINK
ENV GH_LINK=$GH_LINK

ARG SV_DOMAIN
ENV SV_DOMAIN=$SV_DOMAIN

ARG SV_SCHEME
ENV SV_SCHEME=$SV_SCHEME

RUN pkg install git -y

ADD "https://api.github.com/repos/elpekenin/docker-40dex-web/commits?per_page=1" latest_commit
RUN git clone https://github.com/elpekenin/docker-40dex-web && shopt -s dotglob && mv -v docker-40dex-web/* .

RUN date +%d/%m/%Y > build-timestamp

RUN python create-static.py

CMD ["/app/entrypoint.sh"]
