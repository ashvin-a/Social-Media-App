FROM python:3.9
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
COPY ./project /code
WORKDIR /code
RUN pip install -r /tmp/requirements.txt
EXPOSE 8000

