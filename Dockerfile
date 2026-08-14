FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /code
RUN apt-get update
RUN apt-get install -y libxml2-dev libxmlsec1-dev
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install
COPY ./ .
EXPOSE 8000
