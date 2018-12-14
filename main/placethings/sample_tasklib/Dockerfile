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

FROM kumokay/heliot_host:v3

# get tasklib
WORKDIR /opt/github
RUN rm -rf unzip_tasklib
RUN wget https://github.com/nesl/Heliot/raw/dev/main/placethings/sample_tasklib/sample_tasklib.tar.gz
RUN mkdir unzip_tasklib && tar -xzvf sample_tasklib.tar.gz -C unzip_tasklib
RUN rm sample_tasklib.tar.gz

# assign entrypoint workdir
WORKDIR /opt/github/unzip_tasklib
