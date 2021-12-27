#!/bin/bash
echo "Deploy  Frontend Docker image to Local registry"




ls -la
#remove container
docker stop $(docker ps -a | awk '{print $1}')
docker rm -f $(docker stop $(docker ps -a | awk '{print $1}'))

#remove images
docker images -a  | awk '{print $3}' | xargs docker rmi --force
docker images -a | grep "none" | awk '{print $3}' | xargs docker rmi --force
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)

echo "Docker Images before deploy"
docker image ls

docker run -d -p 5000:5000 --restart=always --name registry registry:2

echo "Begin build docker images  "
docker build --no-cache=true -t 10.86.224.30:5000/flack-api .
echo "Finish build docker images  "

echo "Begin Push Images to Local Docker Repository"

docker push "10.86.224.30:5000/flack-api:latest"

echo "Finish Push Images to Local Docker Repository"
docker image ls

echo "Finish Push Images to Local Docker Repository"
docker-compose up -d

exit 0