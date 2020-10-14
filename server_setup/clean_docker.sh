docker system prune -f
docker system prune -f --volumes
docker container prune -f

docker container stop $(docker container ls -aq)
docker container rm $(docker container ls -aq)

docker image prune -a -f
docker volume prune -f
docker network prune -f
