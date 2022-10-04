FROM python:3.10.6
SHELL ["/bin/bash", "-c"]

MAINTAINER Pablo (elpekenin) Martinez Bernal "martinezbernalpablo@gmail.com"

# Download all files
WORKDIR /app
RUN git clone https://github.com/elpekenin/docker-website && shopt -s dotglob && mv -v docker-website/* .

# Install dependencies
RUN pip3 install -r requirements.txt

# Save build time
RUN date +%d/%m/%Y > build-timestamp

CMD ["/app/entrypoint.sh"]
