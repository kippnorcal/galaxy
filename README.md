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

**dev environment**
```
SECRET_KEY=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
TABLEAU_TRUSTED_URL=
USER_DOMAIN=
SAML_ENTITY_ID=
SAML_URL=
SAML_SLO=
SAML_CERT=
ROLLBAR_TOKEN=
APP_DOMAIN=
```

**prod environment**
same as dev but also add:
```
SSL=1
ALLOWED_HOSTS=[]
```

Generating a unique secret key can be done via Django:

```python
from django.core.management.utils import get_random_secret_key 
get_random_secret_key()
```

5. Build Docker Image

```
$ docker-compose build
```

### Running the Server

**dev environment**
```
$ docker-compose up -d
```

**prod environment**
```
$ docker-compose -f docker-compose.prod.yml up -d
```
**Note**: The first time running docker-compose you may get an error about the database not being available. Just run `docker-compose down` and then rerun `docker-compose up`.


### Running Database Migrations

```
$ docker-compose run web python manage.py migrate
```

### Create a superuser (if starting fresh)

```
$ docker-compose run web python manage.py createsuperuser
```

### Export data from another instance
**Note**: `docker-compose` must be up to run the following command(s)
```
$ docker-compose exec web python manage.py dumpdata --indent 2 --exclude=contentypes >> db.json
```

Copy the `db.json` file to your new repo

### Import data from another instance

```
$ docker-compose exec web python manage.py loaddata db.json
```

### Taking the server down

```
$ docker-compose down
```

### Running unittest (server must be running)

```
$ docker-compose run web python manage.py test
```

### Running pytest (server must be running)

```
$ docker-compose run web pytest
```

### Collect static files for production

```
$ docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```

