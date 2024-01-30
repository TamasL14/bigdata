FROM python:3.10-slim

ARG DEV_MODE=True
ENV DEV_MODE ${DEV_MODE}
ENV TEST_MODE False

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "app.app", "--host", "0.0.0.0", "--port", "8080"]

