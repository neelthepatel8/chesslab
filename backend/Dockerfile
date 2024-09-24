FROM --platform=linux/amd64 python:3.11.9-alpine
WORKDIR /app
COPY requirements.txt .
RUN apk add --no-cache make
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["make"]
