FROM python:3.8-slim-buster

WORKDIR /opt/app
COPY ./ /opt/app/

RUN rm -rf /opt/app/venv

RUN apt-get update
RUN apt-get -y install gcc

ENV VIRTUAL_ENV=/opt/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3.8 -m venv $VIRTUAL_ENV

RUN pip install -r requirements.txt

EXPOSE 8000
