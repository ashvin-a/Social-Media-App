FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev
COPY ./project /code
WORKDIR /code
RUN pip install -r /tmp/requirements.txt
EXPOSE 8000

