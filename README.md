[![Coding time tracker](https://wakatime.com/badge/github/dominikbullo/sport_club_management_system.svg)](https://wakatime.com/badge/github/dominikbullo/sport_club_management_system)
[![CodeFactor](https://www.codefactor.io/repository/github/dominikbullo/sportagenda/badge?s=a10ccabebcfcd8c21b1fd55e2bb9e5a958d28dd4)](https://www.codefactor.io/repository/github/dominikbullo/sportagenda)
[![Actions Status](https://github.com/dominikbullo/SportAgenda/workflows/Build%20&%20Publish%20to%20registry/badge.svg)](https://github.com/dominikbullo/SportAgenda/actions)
![Language](https://img.shields.io/static/v1?label=Language&message=Python&color=blue)

# Sport Agenda
Web app for complete managing a sport clubs. Events, recording child statistics by time, calculating payouts for coaches and so on...

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
### Prerequisites

In order to run this container you'll need [Docker](https://docs.docker.com/install/#desktop) and [Docker Compose](https://docs.docker.com/compose/install/) installed.
#### Docker
* [Windows](https://docs.docker.com/docker-for-windows/install/)
* [Mac](https://docs.docker.com/docker-for-mac/install/)
* [Linux](https://docs.docker.com/install/#server)

#### Docker Compose
**On desktop systems like Docker Desktop for Mac and Windows, Docker Compose is included as part of those desktop installs.**

* [Manual](https://docs.docker.com/mac/started/)


## Development

Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/). Start your virtual machines with the following shell command:

```
docker-compose up --build
```

If all works well, you should be able to create an admin account with:

```
docker-compose run --rm backend python manage.py createsuperuser
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
docker-compose run --rm backend python manage.py test
```

### And coding style tests

Explain what these tests test and why

```
docker-compose run --rm backend flake8 --exit-zero  --statistics
```

## Deploy app


For production you'll need to fill out `.env` file and use
`docker-compose-prod.yml` file:

    $ docker-compose -f docker-compose-prod.yml up --build -d


The app will then be available at http://localhost:8000

## Built With

* [Docker](https://www.docker.com/)
* [12 Factor](http://12factor.net/)
* Template: [Vuexy](https://pixinvent.com/demo/vuexy-vuejs-admin-dashboard-template/landing/)
* Frontend: [Vue.js](https://vuejs.org/) + [Vue Cli](https://cli.vuejs.org/) + [PWA](https://developers.google.com/web/progressive-web-apps/)
* Backend: [Django](https://www.djangoproject.com/)
* Database: [PostgreSQL](https://ww.postgresql.org/)
* Server: [Nginx](https://nginx.org/)
* API:  [Django REST Framework](https://www.django-rest-framework.org/)

## Versioning

I use [Bumpversion](https://github.com/c4urself/bump2version) for versioning. For the versions available, see the
[Releases on this repository](https://github.com/dominikbullo/sport_club_management_system/releases) or if you need more details you could check you
[Tags on this repository](https://github.com/dominikbullo/sport_club_management_system/tags).

## Authors

* **Dominik Bullo** - *Initial work & idea* - [dominikbullo.sk](http://dominikbullo.sk/)

## License

This project is licensed under the GPL License - see the [LICENSE](LICENSE) file for details
