FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk add gcc musl-dev libffi-dev openssl-dev

RUN pip3 install --no-cache-dir flask gunicorn[gevent]==19.9.0 connexion requests oslash

COPY api /usr/src/app/api
COPY tx-utils/src /usr/src/app

EXPOSE 8080

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "--worker-class", "gevent", "api.server:create_app()"]

