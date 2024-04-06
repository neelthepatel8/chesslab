FROM python:3.11.9-alpine

WORKDIR /app

COPY requirements.txt .
COPY Makefile .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apk add --update make

EXPOSE 8000

CMD ["make"]
