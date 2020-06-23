# Images python on base Ubuntu
FROM tiangolo/uvicorn-gunicorn-starlette:python3.8

# set work directory
WORKDIR /home/app

# install dependencies for container
RUN apt-get update && apt-get install -y netcat

# install dependencies for app
COPY ./app/requirements.txt /home/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy script
COPY ./docker/python/wait_for_service.sh /home/script/wait_for_service.sh

COPY /app /app