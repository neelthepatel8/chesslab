FROM node:18-alpine AS base

WORKDIR /app 

COPY package*.json ./

RUN npm install 

COPY . .

ENV NEXT_PUBLIC_WEBSOCKET_URL "ws://127.0.0.1:8000/ws"

EXPOSE 3000

CMD ["npm", "run", "dev"]
