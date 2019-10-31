FROM python:3-alpine as base

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk add openssl
RUN openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/C=US/ST=North Carolina/L=Chapel Hill/O=UNC Chapel Hill/OU=RENCI/CN=pdsb"

RUN pip3 install --no-cache-dir flask gunicorn connexion

COPY api /usr/src/app/api

EXPOSE 8080

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "--certfile", "cert.pem", "--keyfile", "key.pem", "api.server:create_app()"]


