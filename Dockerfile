FROM python:3.11-slim
WORKDIR /app
RUN addgroup --system app && adduser --system --group app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY ./backend .
COPY ./entrypoint.sh /

RUN chmod +x /entrypoint.sh