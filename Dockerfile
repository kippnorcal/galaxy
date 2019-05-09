FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update
RUN apt-get install -y libxml2-dev libxmlsec1-dev
RUN pip install pipenv
COPY Pipfile /code/
RUN pipenv install --skip-lock
COPY *.py /code/
COPY data_portal/ /code/
