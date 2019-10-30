FROM python:3-alpine

RUN pip3 install --no-cache-dir pytest requests

RUN mkdir /test

WORKDIR /test

COPY test_func.py /test/test_func.py

ENTRYPOINT ["pytest"]
CMD ["-s"]
