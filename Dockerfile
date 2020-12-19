FROM python:3.7-alpine

WORKDIR /app
ADD . /app

RUN apk update && apk add linux-headers postgresql-dev gcc python3-dev musl-dev

RUN pip install -r requirements.txt

RUN chmod +x /app/app-entrypoint.sh

CMD python manage.py db migrate && python manage.py db upgrade

ENTRYPOINT ["/app/app-entrypoint.sh"]
EXPOSE 5000
