FROM python:3.11.3-slim

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY . /app

RUN apt-get update && apt-get install -y git
RUN pip install --upgrade pip build hatchling
RUN pip install -e .
