# No Frontend App

> Well, not really, but the main idea that there was not written a single line of JS to make app feel like it is a modern site that works without page reloading.
>
> ![App Example](no-frontend-movie.gif)

## Technology

1. UP for making site interactive https://unpoly.com
2. Chota for minimal CSS styling https://jenil.github.io/chota/
3. Django as a server

## How to run locally

The project is Dockerized, so I am expecting that Docker and docker-compose are installed on your machine.

1. `make setup`
2. `make migrate`
3. `make docker-manage cmd=createsuperuser`
4. `docker-compose up`
