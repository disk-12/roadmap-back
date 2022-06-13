FROM python:3.8-slim

WORKDIR /usr/src

COPY . .
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", ":8080", "--workers", "1" , "--threads", "8", "app.main:app"]