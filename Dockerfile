FROM python:3.11.4-slim
RUN mkdir -p /home/online_store
RUN addgroup --system online_store && adduser --system --group online_store

ENV HOME=/home/online_store
ENV APP_HOME=/home/online_store/backend
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/backend_static
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./.env ./myagkoe_mesto/.env
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /home/online_store/backend/entrypoint.sh
RUN chmod +x /home/online_store/backend/entrypoint.sh
COPY . .
RUN mkdir -p /home/online_store/backend/backend_static
RUN mkdir -p /home/online_store/backend/backend_media
