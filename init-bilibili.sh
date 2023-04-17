#!/bin/bash

docker build . -t bilibili-auto

docker run --rm -it bilibili-auto