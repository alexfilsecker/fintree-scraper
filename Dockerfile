FROM python:latest

RUN apt-get update \
    && apt-get install -y wget unzip \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && google-chrome-stable_current_amd64.deb \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

