FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

ENV PORT 80

CMD ["python","-m","flask","run","--host","0.0.0.0"]

