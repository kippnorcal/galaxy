FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY Pipfile* /code/
RUN pip install pipenv
RUN pipenv install
COPY *.py /code/
COPY data_portal/ /code/
