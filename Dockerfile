FROM python:3.7-alpine

WORKDIR /app
ADD . /app

RUN apk update && apk add linux-headers postgresql-dev gcc python3-dev musl-dev

RUN python3 -m venv env
RUN source env/bin/activate
RUN pip install -r requirements.txt

RUN chmod +x /app/app-entrypoint.sh

ENTRYPOINT ["/app/app-entrypoint.sh"]
EXPOSE 5000