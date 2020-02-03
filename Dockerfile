FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /code
RUN apt-get update
RUN apt-get install -y libxml2-dev libxmlsec1-dev
RUN pip install pipenv
COPY Pipfile .
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
COPY ./ .
EXPOSE 8000
