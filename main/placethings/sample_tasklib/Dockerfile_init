############################################################
# How to use this file:
#
# To build/update this image from where it stopped last time
#     sudo docker build -t yourhubusername/imagename:version .
# To build this image from the beginning
#     sudo docker build --no-cache -t yourhubusername/imagename:version .
# To upload your image to dockerhub
#     sudo docker push yourhubusername/imagename:version
# To run this image
#     sudo docker run -it yourhubusername/imagename:version /bin/bash
#
# To test if placethings.main_entity works
# (1) in the docker command line:
#   root@docker:/opt/github/placethings# ifconfig eth0
#   eth0      Link encap:Ethernet  HWaddr 02:42:ac:12:00:08
#             inet addr:172.18.0.8  Bcast:172.18.255.255  Mask:255.255.0.0
#   root@docker:/opt/github/placethings# python main_entity.py run_task -n task_camera -en task_forward -a 172.18.0.8:18800
# (2) outside of docker, do
#   $ python main_entity.py run_client -n client -a 172.18.0.8:18800 -m push -al "this is a test msg"
# (3) check if the task inside the docker receives the message
############################################################

# start from an official ubuntu image
FROM ubuntu:16.04

# install some tools
RUN apt-get update
RUN apt-get -y install git wget vim iputils-ping net-tools

# install python packages for main_entity.py only
RUN apt-get -y install python-pip
RUN pip install --upgrade pip==9.0.1
RUN pip install msgpack-rpc-python Pillow future Flask

# create a working directory
RUN mkdir -p /opt/github

# install yolov3
WORKDIR /opt/github
RUN git clone https://github.com/pjreddie/darknet
WORKDIR /opt/github/darknet
RUN make
RUN wget https://pjreddie.com/media/files/yolov3.weights
RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights

# get tasklib
WORKDIR /opt/github
RUN wget https://github.com/nesl/Heliot/raw/dev/main/placethings/sample_tasklib/sample_tasklib.tar.gz
RUN mkdir unzip_tasklib && tar -xzvf sample_tasklib.tar.gz -C unzip_tasklib
RUN rm sample_tasklib.tar.gz

# assign entrypoint workdir
WORKDIR /opt/github/unzip_tasklib
