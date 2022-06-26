# /bin/sh
pip install -e .
pytest
poetry run pflake8