FROM python:3.11
LABEL maintainer="Pablo (elpekenin) Martinez Bernal"
LABEL email="martinezbernalpablo@gmail.com"
WORKDIR /app

ARG DB_URI
ENV DB_URI=$DB_URI

ARG GH_LINK
ENV GH_LINK=$GH_LINK

ARG SV_DOMAIN
ENV SV_DOMAIN=$SV_DOMAIN

ARG SV_SCHEME
ENV SV_SCHEME=$SV_SCHEME

RUN apt update && apt install git

ADD "https://api.github.com/repos/elpekenin/docker-40dex-web/commits?per_page=1" latest_commit
RUN git clone https://github.com/elpekenin/docker-40dex-web && cp -r docker-40dex-web/* . && mv docker-40dex-web/.git . && rm -rf docker-40dex-web
RUN pip3 install -r requirements.txt

RUN date +%d/%m/%Y > build-timestamp

RUN python3 create-static.py

CMD ["/app/entrypoint.sh"]
