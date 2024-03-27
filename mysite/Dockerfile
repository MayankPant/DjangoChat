FROM python:3.9-buster

RUN apt-get update && apt-get install -y libpq-dev
RUN pip install --upgrade pip

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .

EXPOSE 8000
# using uvicorn as an asgi server aided by gunicorn for process monitoring
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "mysite.asgi:application"]