FROM python:3.8.0

WORKDIR /twt-traffic

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "python", "stream/Streaming.py" ]