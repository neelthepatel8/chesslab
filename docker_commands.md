## Build:

` docker-compose up -d  `

## Tag:

`   docker tag game-backend:latest 541032831567.dkr.ecr.us-east-2.amazonaws.com/chessgame:latest-backend   `
`   docker tag game-frontend:latest 541032831567.dkr.ecr.us-east-2.amazonaws.com/chessgame:latest-frontend   `

## Push

`    docker push 541032831567.dkr.ecr.us-east-2.amazonaws.com/chessgame:latest-backend   `
`    docker push 541032831567.dkr.ecr.us-east-2.amazonaws.com/chessgame:latest-frontend   `

## Pull on AWS:

`  docker pull 541032831567.dkr.ecr.us-east-2.amazonaws.com/chessgame:latest-backend   `
`  docker pull 541032831567.dkr.ecr.us-east-2.amazonaws.com/chessgame:latest-frontend   `

## Run on AWS:

`  docker compose up -d  `
