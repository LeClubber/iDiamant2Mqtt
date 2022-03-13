FROM python:3-alpine

ENV MQTT_PORT 1883
ENV MQTT_HOST mqtt
ENV MQTT_TOPIC homeassistant
WORKDIR /usr/src/idiamant

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "-u", "server.py"]