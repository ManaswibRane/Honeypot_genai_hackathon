FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN mkdir -p logs

RUN pip install --no-cache-dir paramiko cryptography

EXPOSE 2222

CMD ["python", "-u", "-m", "ssh_server.session_handler"]
