# Heliot: Hybrid Emulation of Learning Enabled IoT systems


**Heliot** is a framework to emulate different IoT scenarios. An Iot scenario in Heliot consists of sensors (both real and virtual), compute resources (cloud, cloudlet, edge devices, containers etc) running computation and a dynamic network topology.  Heliot simplifies to study the application performance in presence of heterogeneous compute resources, sensors, dynamic network characteristics,and compute partition and placement algorithms. Heliot is in active development. 

<br />

To better understand the Heliot, let us consider a demo IoT scenario of surveillance as follows.

![Demo Surveillance Scenario](https://github.com/nesl/Heliot/blob/master/docs/images/Demo_Arch_1.png)

In this scenario, we have two image sensors capturing images on which object detection is done in realtime. 

The scenario consists of the following components:
- Object detection inference of detecting Cars and Person from images using Neural Network.
- Two image sensors (i) **Google Vision Kit**  (ii) **Drone** in Airsim having Camera.
- Compute resources (Google Vision Kit, Virtual Container, Nvidia Jetson TX-2). At present, the inference is done on Nvidia Jetson TX-2. 
- Network emulation using **Mininet**.
- User **Smartphone** to deliver the notification.

<br />

# Installation and System Setup
In order to emulate the demo surveillance scenario, we will setup the below system. The installation steps are listed separately for each section.

- **Nvidia Jetson-TX2**: [Nvidia Jetson-TX2](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems-dev-kits-modules/) will act as an edge server having GPU (local accelerator). 
  - System and Installation steps: [Available here](https://github.com/nesl/Heliot/tree/master/computation/Jetson).

- **Google Vision Kit**:
  - System and Installation steps: [Available here](https://github.com/nesl/Heliot/blob/master/sensor/RaspberryPi/Readme.md)

- **Windows machine running Airsim**: Our goal is to setup a drone in AirSim having camera sensor. 
  - System and Installation steps: [Available here](https://github.com/nesl/Heliot/blob/master/sensor/AirSim/Readme.md)

- **Ubuntu machine running Mininet**:
  - System and Installation steps: [Available here](https://github.com/nesl/Heliot/blob/master/network/Mininet/Readme.md)

# Running Demo Scenario

<!--Currently Heliot is still under development. -->
 Heliot is in active development.
Please follow the installation and system set up steps listed above. 

## 1. Inference on Jetson-Tx2
In the folder Heliot/computation/Jetson/ run.
```
python3 main.py
```

<br/>
To verify, that Jetson-Tx2 is running as inference server run.

```
python3 test.py
```

Note: add instructions for Tx2 to update the ip.
 
## 2. Running Mininet
<!-- Please get the source code from our development branch and follow the steps for installation:  -->

1. Install containernet
```
$ sudo apt-get install ansible git aptitude
$ git clone https://github.com/containernet/containernet.git
$ cd containernet/ansible
$ sudo ansible-playbook -i "localhost," -c local install.yml
$ cd ..
$ sudo python setup.py install
$ sudo py.test -v mininet/test/test_containernet.py
```

2. Intall ilp solvers and python packages
```
$ pip install --upgrade pip==9.0.1
$ sudo pip install msgpack-rpc-python numpy Pillow future networkx matplotlib six aenum pulp
$ sudo apt-get install glpk-utils
```

3. get source code from our development branch
```
git clone https://github.com/kumokay/placethings
```

4. modify the config file
```
in placethings/config_ddflow_demo/task_data.json

change the ip addresses and to the correct ip addresses
172.17.51.1:18900 => your actuator that handles the alert message
172.17.49.60:18800 => your edge device with GPU
172.17.51.1:18800 => your general purpose server
```

5. run demo case
```
python main.py -tc test_ddflow_demo.TestDynamic -c config_ddflow_demo
```

## 3. Google Vision Kit as Camera Sensor

In the folder *Heliot/sensor/RaspberryPi/*   run.
<br/> 
Note: add details to update the ip of consumer of images.
``` bash
python3 main.py 
```

## 4. Virtual drone in AirSim as Camera Sensor
In the folder *Heliot/sensor/AirSim* run.
Note: add the updated AirSim code.
``` bash
python3 main.py 
```

## 5. User Smartphone for notification
ToDo.
