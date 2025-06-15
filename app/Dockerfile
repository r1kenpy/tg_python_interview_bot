FROM python:3.12.11-alpine

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY /app .

CMD ["python3", "main.py"]