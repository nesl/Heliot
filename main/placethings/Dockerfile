# Use an official Python runtime as a parent image
FROM kumokay/ubuntu_wifi:v4

# install some tools
RUN apt-get -y install git wget vim
RUN apt-get -y install iputils-ping

# install python packages
RUN apt-get -y install python-pip
RUN pip install --upgrade pip
RUN pip install msgpack-rpc-python
RUN pip install numpy
RUN pip install Pillow
RUN pip install future
RUN pip install aenum

RUN mkdir -p /opt/github
WORKDIR /opt/github
RUN git clone https://github.com/kumokay/placethings.git

RUN git clone https://github.com/pjreddie/darknet
WORKDIR /opt/github/darknet
RUN make
RUN wget https://pjreddie.com/media/files/yolov3.weights
RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights

# assign entrypoint workdir
WORKDIR /opt/github/placethings
RUN git pull
RUN date > date.txt
