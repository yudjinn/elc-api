# Pull base image
FROM python:3.9

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src/

# Install dependencies
COPY requirements.txt /src/
RUN python3 -m pip install -r requirements.txt

COPY ./src /src/

RUN alembic upgrade head

EXPOSE 8000