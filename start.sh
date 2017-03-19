#!/bin/bash
docker build . -t zookeeper_img
if [[ $1 == "web-server" ]]; then 
	echo "Starting webserver..."	
	docker run -v $PWD/src:/tmp/src -v $PWD/zookeeper-3.3.6:/tmp/zookeeper-src -p 8000:8000 -i -t zookeeper_img bash
elif [[ $1 == "zookeeper" ]]; then
	docker run -v $PWD/src:/tmp/src -v $PWD/zookeeper-3.3.6:/tmp/zookeeper-src -i -t zookeeper_img ../zookeeper-src/bin/zkServer.sh start-foreground
else
	docker run -v $PWD/src:/tmp/src -v $PWD/zookeeper-3.3.6:/tmp/zookeeper-src -i -t zookeeper_img bash
fi
