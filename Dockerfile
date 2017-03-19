FROM base_img
RUN apt-get update
RUN apt-get -y install default-jdk
RUN apt-get -y install python-pip
RUN pip --proxy="http://172.30.0.10:3128" install kazoo
RUN pip --proxy="http://172.30.0.10:3128" install django
RUN apt-get -y install vim curl
RUN mkdir /tmp/zookeeper-src
WORKDIR /tmp/src
