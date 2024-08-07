FROM python:3.10-bullseye

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends make \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
