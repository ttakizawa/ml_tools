build:
	docker build -t ml_tools .

test-code:
	docker run -ti --rm -v $(pwd):/usr/src -w /usr/src ml_tools pytest

flake8:
	docker run -ti --rm -v $(pwd):/usr/src -w /usr/src ml_tools poetry run pflake8

check:
	make build
	make test-code
	make flake8