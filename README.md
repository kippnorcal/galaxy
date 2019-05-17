# galaxy
Data Portal web app

## Dependencies

* Python3.7
* Django 2.2
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)
* [Docker](https://www.docker.com/)

## Getting Started

### Setup Environment

1. Clone this repo

```
$  git clone https://github.com/kipp-bayarea/galaxy.git
```

2. Install Pipenv

```
$ pip install pipenv
```

3. Install Docker

* **Mac**: [https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/)
* **Linux**: [https://docs.docker.com/install/linux/docker-ce/debian/](https://docs.docker.com/install/linux/docker-ce/debian/)
* **Windows**: [https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/)

4. Create .env file with project secrets
```
SECRET_KEY=''
POSTGRES_USER=
POSTGRES_DB=
POSTGRES_PASSWORD=
SAML_ENTITY_ID''
SAML_URL=''
SAML_CERT=''
```

5. Build Docker Image

```
$ docker-compose build
```

### Running the Server

```
$ docker-compose up
```
**Note**: The first time running docker-compose you may get an error about the database not being available. Just run `docker-compose down` and then rerun `docker-compose up`.

### Running Database Migrations

```
$ docker-compose run web pipenv run python manage.py migrate
```

### Create a superuser

```
$ docker-compose run web pipenv run python manage.py createsuperuser
```

### Running Tests

```
$ docker-compose run web pipenv run python manage.py test
```

