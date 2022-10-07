FROM python:3.10.6
SHELL ["/bin/bash", "-c"]

MAINTAINER Pablo (elpekenin) Martinez Bernal "martinezbernalpablo@gmail.com"

ARG DB_URI
ENV DB_URI=$DB_URI

ARG SV_DOMAIN
ENV SV_DOMAIN=$SV_DOMAIN

ARG SV_SCHEME
ENV SV_SCHEME=$SV_SCHEME

# Download all files
WORKDIR /app
RUN git clone https://github.com/elpekenin/docker-40dex-web && shopt -s dotglob && mv -v docker-40dex-web/* .

# Install dependencies
RUN pip3 install -r requirements.txt

# Store build time
RUN date +%d/%m/%Y > build-timestamp

# Create static 40dex HTML
RUN python create-static.py

CMD ["/app/entrypoint.sh"]
