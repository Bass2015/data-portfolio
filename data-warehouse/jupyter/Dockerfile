FROM jupyter/datascience-notebook:latest

USER root

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    apt-get clean && rm -rf var/lib/apt/lists/*

RUN pip install --no-cache-dir ipython-sql sqlalchemy psycopg2

VOLUME /notebooks

WORKDIR /notebooks