FROM python:3.8
WORKDIR /usr/src/app/
COPY . .
CMD [ "python", "blattidus.py", "-p", "5080", "-r", "." ]
