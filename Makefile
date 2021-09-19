# ENV defaults to local (so that requirements/local.txt are installed), but can be overridden
#  (e.g. ENV=production make setup).
ENV ?= local
# PYTHON specifies the python binary to use when creating virtualenv
PYTHON ?= python3.9

# Editor can be defined globally but defaults to nano
EDITOR ?= nano

# By default we open the editor after copying settings, but can be overridden
#  (e.g. EDIT_SETTINGS=no make settings).
EDIT_SETTINGS ?= yes

# Project name
PROJECT_NAME ?= app

# Get root dir and project dir
PROJECT_ROOT ?= $(CURDIR)
SITE_ROOT ?= $(PROJECT_ROOT)/$(PROJECT_NAME)

CUR_DIR_NAME ?= $(shell basename `pwd`)

.PHONY:
all: help


.PHONY:
help:
	@echo "+------<<<<                                 Configuration                                >>>>------+"
	@echo ""
	@echo "ENV: $(ENV)"
	@echo "PYTHON: $(PYTHON)"
	@echo "PROJECT_ROOT: $(PROJECT_ROOT)"
	@echo "SITE_ROOT: $(SITE_ROOT)"
	@echo ""
	@echo "+------<<<<                                     Tasks                                    >>>>------+"
	@echo ""
	@grep --no-filename -E '^[a-zA-Z_%-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""

.PHONY:
docker:
	@docker-compose down
	@docker-compose build
	@docker-compose up -d
	@docker-compose logs -f


.PHONY:
setup: ## Sets up the project in your local machine
	@echo "Creating Docker images"
	@docker-compose build
	@echo "Running django migrations"
	@make migrate
	@echo "===================================================================="
	@echo "SETUP SUCCEEDED"


$(PROJECT_ROOT)/.env:
	@echo "Copying .env file"
	@cp $(PROJECT_ROOT)/.env.example $(PROJECT_ROOT)/.env


.PHONY:
clean:
	@echo "Cleaning pyc files"
	@make run-python cmd='find . -name "*.pyc" -exec rm -rf {} \;'


.PHONY:
psql:
	docker-compose exec postgres psql --user $(PROJECT_NAME) --dbname $(PROJECT_NAME)


.PHONY:
docker-django:
	docker-compose run --rm app $(cmd)


.PHONY:
django-shell:
	docker-compose run --rm app bash


.PHONY:
docker-manage:
	docker-compose run --rm app ./manage.py $(cmd)


.PHONY:
shell:  ## Drop into Django shell
	docker-compose run --rm app ./manage.py shell


.PHONY:
makemigrations migrations:  ## Generate new DB migrations
	docker-compose run --rm app ./manage.py makemigrations $(cmd)


.PHONY:
migrate:  ## Apply DB migrations
	docker-compose run --rm app ./manage.py migrate $(cmd)


PYTHON_DOCKER_IMAGE ?= "tg-hug_app"

# NOTE:
# Do not use `docker-compose run` to avoid spawning services by the app container
.PHONY:
run-python:
	@set -e ;\
	if [ "`docker images|grep $(PYTHON_DOCKER_IMAGE)`" = '' ]; then \
	    docker-compose build app || exit $$?; \
	fi; \
	docker run -t --rm -v $(PROJECT_ROOT)/app:/app $(PYTHON_DOCKER_IMAGE) $(cmd)


.PHONY:
black-check:
	@make run-python cmd="black --check --diff $(cmd)"


.PHONY:
black-check-all:
	@make run-python cmd="black --check --diff ."


.PHONY:
black-format:
	@make run-python cmd="black $(cmd)"


.PHONY:
black-format-all:
	@make run-python cmd="black ."


.PHONY:
lint: black-check-all isort python-lint mypy


.PHONY:
quality: lint poetry-check ## Run quality checks


.PHONY:
fmt: black-format-all isort-fix ## Format Python Files


.PHONY:
python-lint:
	@echo "Running pylint"
	@make run-python cmd="pylint"


.PHONY:
mypy:
	@echo "Checking types"
	@make run-python cmd="mypy --show-error-codes"


.PHONY:
isort:
	@echo "Checking imports with isort"
	@make run-python cmd='isort --check-only -p app --diff'


.PHONY:
isort-fix:
	@echo "Fixing imports with isort"
	@make run-python cmd='isort .'


.PHONY:
coverage: ## Runs python test coverage calculation
	@echo "Running automatic code coverage check"
	@docker-compose run --rm app pytest --cov=. --cov-report html --cov-report xml --cov-report term-missing


.PHONY:
test:  ## Run python test suit
	@echo "Running automatic tests"
	@docker-compose run --rm app py.test
