#FROM ubuntu:16.04
#RUN apt-get update && \
#apt-get install git && \
#git clone -b dev https://github.com/nesl/Heliot.git && \
#CMD ls

#Building a direct docker image
#https://rominirani.com/docker-tutorial-series-part-5-building-your-own-docker-images-b4a448b44afc

Steps:
1) sudo docker pull ubuntu:16.04

2) sudo docker run -it --name heliotDocker ubuntu:16.04
starts the container run the below commands:

apt-get update
apt-get install git
cd home
git clone -b dev https://github.com/nesl/Heliot.git

#install python3 and flask as well
apt-get install python3
apt install python3-pip
pip3 install flask

#installing ping Utilities
apt-get install iputils-ping


3) commit the changes
sudo docker commit heliotDocker sandynesl/heliot:1

4) login into the docker repo
sudo docker login --username=sandynesl

5) Docker push
sudo docker push sandynesl/heliot:1
sudo docker push sandynesl/heliot:2


-------------------Next try from katie Docker-----
sudo docker run -it --name heliotDocker kumokay/ubuntu_wifi:v6


#making changes to heliotDocker

sudo docker rm heliotDocker
sudo docker run -it --name heliotDocker sandynesl/heliot:1
sudo docker commit heliotDocker sandynesl/heliot:1
