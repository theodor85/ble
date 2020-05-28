FROM python:3.8

COPY ./source/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

WORKDIR /app
