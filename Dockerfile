FROM python:3.8-alpine

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
# Python, don't write bytecode!
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apk update \
	&& apk upgrade --no-cache \
	&& apk add --no-cache git \
	&& pip install --no-cache-dir pipenv

COPY Pipfile* ./
RUN pipenv install --deploy --system
COPY app app

ENTRYPOINT uvicorn app.main:app --host 0.0.0.0
EXPOSE 8000