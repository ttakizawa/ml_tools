# /bin/sh
pip install -e .
pytest -s
poetry run pflake8