#!/bin/bash
sudo docker rm -f claraideia-webapp && sudo docker rmi claraideia-web
sudo docker run --name claraideia-webapp --network=uendel_multi-net -p 8000:8000 claraideia-web
