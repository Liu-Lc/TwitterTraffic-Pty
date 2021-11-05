FROM python:3.8.0

RUN mkdir -p /twt-traffic/stream
WORKDIR /twt-traffic/stream

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

CMD [ "python", "Streaming.py" ]