# Parallel Matrix Microservices

## Setup (Debian VM)

### Run Docker without sudo
```sh
sudo usermod -a -G docker $USER
newgrp docker
```

### Start a single-node swarm
```sh
docker swarm init --advertise-addr 10.0.2.15
```

## Build and run
```sh
docker compose build
docker compose up
```

## Stop container
```sh
docker compose down
```
