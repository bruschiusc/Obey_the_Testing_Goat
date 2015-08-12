FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /goat
WORKDIR /goat
ADD requirements.txt /goat/
RUN pip install -r requirements.txt
ADD . /goat/
