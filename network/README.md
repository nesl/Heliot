# Network Emulator

0. Hardware
- General purpose server with Ubuntu Linux 16.04 LTS
- Minimum system requirements:
    * 2 GHz dual core processor or better
    * 2 GB system memory
    * 5 GB of free hard drive space
    * Internet access

1. Install containernet
```
sudo apt-get install ansible git aptitude
git clone https://github.com/containernet/containernet.git
cd containernet/ansible
sudo ansible-playbook -i "localhost," -c local install.yml
cd ..
sudo python setup.py install
sudo py.test -v mininet/test/test_containernet.py
```

2. Install ilp solvers and python packages
```
pip install --upgrade pip==9.0.1
sudo pip install msgpack-rpc-python numpy Pillow future networkx six aenum pulp
sudo pip install matplotlib==2.0.2
sudo apt-get install glpk-utils
```

3. get source code from our development branch and download the sample docker container
```
git clone https://github.com/kumokay/placethings
sudo docker pull kumokay/ubuntu_wifi:v6
```

