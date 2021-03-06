FROM python:3-alpine

WORKDIR /usr/app

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "chipscrape.py"]
