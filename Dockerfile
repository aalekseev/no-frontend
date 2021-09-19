FROM python:3.9-slim-buster

ENV POETRY_VIRTUALENVS_CREATE 0
ENV PYTHONPYCACHEPREFIX /.pycache

# Let all *.pyc files stay within the container, for Python >= 3.8
RUN mkdir -p $PYTHONPYCACHEPREFIX

# Use non-interactive frontend for debconf
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install system requirements
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gettext libpq-dev zlib1g-dev libjpeg62-turbo-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy Python requirements dir and Install requirements
RUN pip install -U pip setuptools wheel poetry

COPY wait-for-it.sh /usr/bin/

COPY app/pyproject.toml /
COPY app/poetry.lock /

# Install all dependencies from poetry.lock (dev included by default)
RUN poetry install

# Set the default directory where CMD will execute
WORKDIR /app

CMD bash
