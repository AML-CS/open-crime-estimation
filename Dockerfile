FROM python:3.8.5-buster

WORKDIR /usr/src

RUN pip3 install wheel gunicorn

COPY ./requirements.txt .
RUN pip3 install  -r requirements.txt

COPY . .

CMD ["gunicorn", "--preload", "-t 600", "wsgi:server"]