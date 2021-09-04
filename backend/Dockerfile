# Pull base image
FROM python:3.7

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend/

# Install dependencies
COPY requirements.txt /backend/
RUN pip install -r requirements.txt

COPY . /backend/

EXPOSE 8000