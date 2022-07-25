FROM python:3.9-slim-buster

RUN apt update && apt install wget git -y
RUN wget https://github.com/mikefarah/yq/releases/download/v4.26.1/yq_linux_arm64.tar.gz -O -|\
    tar xz && mv yq_linux_arm64 /usr/bin/yq

WORKDIR /usr/local/airflow

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -U setuptools wheel pipenv \
    && pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]