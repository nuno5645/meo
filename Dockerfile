FROM ubuntu:22.04

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

RUN apt-get clean && rm -rf /var/lib/apt/lists/* && \
    apt-get update --fix-missing && \
    apt-get install -y python3.11 python3.11-dev python3-pip tzdata nano && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y cron

COPY requirements.txt requirements.txt

RUN python3.11 -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . /src

WORKDIR /src


RUN python3.11 /src/manage.py crontab add
RUN service cron start 

CMD ["uwsgi", "--ini", "/src/config/uwsgi/ws.ini"]