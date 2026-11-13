# Parallel Matrix Microservices

## Initial Setup (Debian VM)

### Run Docker without sudo
```sh
sudo usermod -a -G docker $USER
newgrp docker
```

### Start a single-node swarm
```sh
-- This needs to be done in order to start builds -- 
docker swarm init --advertise-addr 10.0.2.15
```

## How to run a test 
```sh
-- This  will build and Image -- 
docker compose build

-- This will start the containers -- 
docker compose up

-- This will turn off the containers --
docker compose down
```

