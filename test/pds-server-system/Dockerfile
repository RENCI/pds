FROM python:3-alpine as base

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip3 install --no-cache-dir flask gunicorn==19.9.0 connexion

COPY api /usr/src/app/api

EXPOSE 8080

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "api.server:create_app()"]


