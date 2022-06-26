build:
	docker-compose build

test-code:
	docker-compose run --rm --entrypoint pytest ml_tools

flake8:
	docker-compose run --rm --entrypoint "poetry run pflake8" ml_tools

check:
	docker-compose run --rm --entrypoint "sh check.sh" ml_tools

login:
	docker-compose run -ti --rm ml_tools /bin/bash