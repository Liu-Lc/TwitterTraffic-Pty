FROM python:3.8.0

RUN mkdir -p /twt-traffic/stream
WORKDIR /twt-traffic/stream

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY TweetData .
COPY assets .
COPY models .
COPY Streaming.py .

CMD [ "python", "Streaming.py" ]