#!/bin/bash
image_name="care_modle"
tag="v_$(date "+%Y%m%d")"


start_build_image(){
    printf "\n================ Start build ${image_name}:${tag} image ================\n\n"
    echo "start build..."
    docker build -f ./docker/Dockerfile -t "${image_name}:${tag}" .

    docker images | grep "${tag}"
}

clear_container(){
    printf "\n================ delete exit containers ================\n\n"
    docker rm $(docker ps -a | grep "Exit" | awk '{print $1}')
    docker ps -a
    printf "                           ok                              "
}

clear_image(){
    
    printf "\n================ delete None image ================\n\n"
    docker rmi $(docker images | grep "<none>" | awk '{print $3}')
    docker images
    printf "                           ok                              "
}

service(){
    printf "\n================ start service ================\n\n"
    docker run -d -p 31004:8000 --name ${image_name} -v $(pwd)/log:/${image_name}/log -d ${image_name}:${tag}
}

service_docker_compose(){
    pwd
    docker-compose -f ./docker-compose.yml up -d
}

start(){
  start_build_image
#  clear_container
#  clear_image
  #切换到项目上级目录
  service
}


start