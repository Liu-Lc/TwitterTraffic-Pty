FROM python:3.8.0

RUN mkdir -p /twt-traffic/app
WORKDIR /usr/twt-traffic/app

COPY requirements.txt /usr/twt-traffic/app/
RUN pip install -r requirements.txt

COPY app/ /usr/twt-traffic/app/

 CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]