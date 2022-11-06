# syntax=docker/dockerfile:1
FROM python:3.10

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . .

RUN pip install pipenv
RUN pipenv install

ENTRYPOINT ["python", "assistant/assistant/main.py"]