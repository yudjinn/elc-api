# Pull base image
FROM python:3.9

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

# Install dependencies
COPY requirements.txt /app/
RUN python3 -m pip install -r requirements.txt

COPY . /app/

EXPOSE 8000