FROM python:3.8
WORKDIR /usr/src/app/
COPY . .
CMD [ "python", "blattidus.py", "5080", "index.html" ]
