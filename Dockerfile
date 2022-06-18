FROM python:3

WORKDIR /usr/src

COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir setuptools==62.3.4 poetry==1.1.13 && poetry config virtualenvs.create false
RUN poetry install
RUN pip install -e .