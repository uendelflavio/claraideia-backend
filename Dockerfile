FROM python:3.7-alpine

MAINTAINER Uendel Flavio Santos Martins

LABEL "com.example.vendor"="ClaraIdeia"
LABEL com.example.label-with-value="claraideia"
LABEL version="1.0"
LABEL description="Imagem contendo servidor nginx para servir paginas em python com framework fastapi"

ENV PYTHONPATH=/app
ENV MONGO_HOST=10.1.0.2
ENV MONGO_PORT=27017
ENV MONGO_USER=root
ENV MONGO_USERNAME=root
ENV MONGO_PASSWORD=1817698
ENV MONGO_DB=claraideia

COPY . /home/claraideia-webapp
WORKDIR /home/claraideia-webapp
RUN apk add --no-cache --virtual .build-deps gcc libc-dev make libffi-dev \
    && pip install --no-cache-dir --upgrade pip \
    && xargs -n 1 -P 8 pip install --no-cache-dir --no-cache-dir < requirements.txt \    
    && apk del .build-deps
CMD pymongo-migrate migrate -u 'mongodb://MONGO_USER:MONGO_PASSWORD@MONGO_HOST:MONGO_PORT/MONGO_DB?authSource=admin' -m ./migration/ 
CMD python3 start_server.py
EXPOSE 8000