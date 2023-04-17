#!/bin/bash

docker build . -t bilibili-auto
docker run --rm -it -v ${PWD}/cookie.txt:/app/cookie.txt bilibili-auto