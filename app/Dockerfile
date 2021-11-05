FROM python:3.8.0

RUN mkdir -p /twt-traffic/app
WORKDIR /twt-traffic/app

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY TweetData .
COPY assets .
COPY WebDash.py .

 CMD [ "python", "WebDash.py"]