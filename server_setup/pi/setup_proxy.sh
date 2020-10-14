mkdir nginx-proxy && cd nginx-proxy || exit
docker network create nginx-proxy
docker-compose up -d
docker ps
