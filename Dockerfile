FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

CMD ["sh", "docker-entrypoint.sh"]

