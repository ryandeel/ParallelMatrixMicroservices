# Initial Setup (Debian VM)

**Run Docker commands without having to do sudo**
```sh
sudo usermod -a -G docker $USER
newgrp docker
```

**Start a single-node swarm**
```sh
"-- Must do before doing Docker Compose Up --"
docker swarm init --advertise-addr [INSERT ROUTABLE NETWORK ADDRESS HERE], such as an en interface like enp0s3 and NOT lo
```

# How to run a test 
```sh
"-- This  will build and Image --"
docker compose build

"-- This will start the containers --"
docker compose up

"-- This will turn off the containers --"
docker compose down
```
