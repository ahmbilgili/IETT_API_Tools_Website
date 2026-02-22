# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7



# docker build -t iett_api_website --platform=linux/amd64 -f app/Dockerfile .
# --platform sets the platform to amd64
# -f sets the location of dockerfile, so that you can work in your current context (.) instead of context ./app
FROM python:3.15.0a5-alpine3.23

COPY ./app ./requirements.txt ./app
RUN apk update && apk add build-base && apk add libxml2-dev libxslt-dev && pip install -r app/requirements.txt
WORKDIR app
EXPOSE 80
CMD gunicorn --bind 0.0.0.0:80 app:app
