FROM node:18-alpine AS base

WORKDIR /app 

COPY package*.json ./

RUN npm install 

COPY . .

ENV NEXT_PUBLIC_WEBSOCKET_URL "ws://ChessDevLoadBalancer-1437957295.us-east-1.elb.amazonaws.com:8000/ws"

EXPOSE 3000

CMD ["npm", "run", "dev"]
