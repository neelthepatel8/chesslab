FROM node:18-alpine AS base

WORKDIR /app 

COPY package*.json ./

RUN npm install 

COPY . .

ENV NEXT_PUBLIC_WEBSOCKET_URL "ws://ec2-3-131-218-211.us-east-2.compute.amazonaws.com:8000/ws"

EXPOSE 3000

CMD ["npm", "run", "dev"]
