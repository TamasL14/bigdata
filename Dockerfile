FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN apt-get update &&\
    apt-get install -y libmagic-dev

RUN pip install -r requirements.txt

COPY app/ .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]