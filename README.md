# ZookeeperDemo
Steps to setup the environment:
  1. Install Docker
  2. Download apache zookeeper-3.3.36 if the zookeeper directory already present in the project folder is corrupt
  3. Build "base_img" image from base_img directory
  4. Run start.sh for building the image with required tools

NOTE: Dockerfile is written such that it uses college proxy. Remove the proxy setting in dockerfile if you want to make it work
outside college.
 
 Command to start Zookeeper: ./start.sh zookeeper
 Command to start webserver: ./start.sh web-server
 Command to start db server: ./start.sh db-server
 
 Port 8000 of webserver container is mapped to port 8000 of host, so in order to make request to webserver, use "127.0.0.1:8000/testapp" as the url
 
 #For read: http://127.0.0.1:8000/testapp/read/id/
 
 #for update: http://127.0.0.1:8000/testapp/update/id/new_value
