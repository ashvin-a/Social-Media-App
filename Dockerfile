FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
WORKDIR /code
RUN apk add --update --no-cache postgresql-client && \
	apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev && \
	adduser --disabled-password --gecos '' ashvin && \
	chown -R ashvin:ashvin /code/ 
RUN pip install -r /tmp/requirements.txt
COPY ./project /code
USER root
RUN	chown -R ashvin:ashvin /code/media/profile_images/
USER ashvin
EXPOSE 8000

