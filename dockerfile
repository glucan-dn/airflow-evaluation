FROM apache/airflow:latest
USER root
RUN apt update && apt install -y vim
RUN pip install dag-factory
USER airflow