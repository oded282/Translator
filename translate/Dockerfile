FROM python:3.7-stretch

WORKDIR /var/www

ADD . /var/www

RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]