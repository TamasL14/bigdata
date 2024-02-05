FROM python:3.12

WORKDIR /app

VOLUME ["/tmp/uploads"]

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

COPY app/ .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]