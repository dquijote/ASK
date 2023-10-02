# The image you are going to inherit your Dockerfile from
FROM ubuntu:focal
# Necessary, so Docker doesn't buffer the output and that you can see the output 
# of your application (e.g., Django logs) in real-time.
ENV PYTHONUNBUFFERED 1
# Make a directory in your Docker image, which you can use to store your source code
RUN mkdir /django_ASK
# Set the /django_recipe_api directory as the working directory
WORKDIR /django_ASK
# Copies from your local machine's current directory to the django_recipe_api folder 
# in the Docker image
#COPY . .
# Copy the requirements.txt file adjacent to the Dockerfile 
# to your Docker image
COPY ./requirements.txt /requirements.txt

ENV http_proxy=http://fvelazquez:Liebe07pe.@10.7.1.48:8080
ENV https_proxy=https://fvelazquez:Liebe07pe.@10.7.1.48:8080
RUN apt-get update && apt-get install -y python3 --no-install-recommends
RUN apt-get install python3-pip -y --no-install-recommends
# Install the requirements.txt file in Docker image
RUN pip install -r /requirements.txt
# Create a user that can run your container
RUN rm -rf /var/lib/apt/lists/*
RUN adduser user
USER user
#RUN python3 gym/manage.py runserver