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
############################################################

# start from an official ubuntu image
FROM ubuntu:16.04

# install some tools
RUN apt-get update
RUN apt-get -y install git wget vim iputils-ping

# install python packages for main_entity.py only
RUN apt-get -y install python-pip
RUN pip install --upgrade pip==9.0.1
RUN pip install msgpack-rpc-python numpy Pillow future six aenum

# create a working directory
RUN mkdir -p /opt/github

# install yolov3
WORKDIR /opt/github
RUN git clone https://github.com/pjreddie/darknet
WORKDIR /opt/github/darknet
RUN make
RUN wget https://pjreddie.com/media/files/yolov3.weights
RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights

# get placethings (for main_entity.py only)
WORKDIR /opt/github
RUN git clone https://github.com/kumokay/placethings.git

# assign entrypoint workdir
WORKDIR /opt/github/placethings
