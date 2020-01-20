FROM python:3.7

RUN pip install gunicorn

COPY docker/settings.ini /app/kbsbot/channel_handler/settings.ini

COPY . /app

RUN pip install -r /app/requirements.txt
RUN pip install /app/

WORKDIR /app/kbsbot/channel_handler

ENV COMPOSE_ENGINE="http://127.0.0.1:5000"
ENV KEY="9WhoO2zEai7PveqOKEbatLobHCj45FLci6rtROxqpE4="

EXPOSE 8005
CMD ["gunicorn", "-b", "0.0.0.0:8005", "run:app"]


