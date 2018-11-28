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

---
---

# System Requirements
## 1. Host-1 (AirSim machine)
-  **Hardware requirements** 
   - Recommended configuration: Intel core i9 or i7 processor with 8 cores, 32 GB RAM, NVIDIA TitanX GPU and peripherals (monitor, mouse, and keyboard).
   - For development purpose, we use i7 processor with 8 cores, 32 GB RAM and NVIDIA TitanX GPU. 
- **Operating system** : [Windows 10 Home](https://www.microsoft.com/en-us/software-download/windows10ISO).


## 2. Host-2 (Mininet machine)
-  **Hardware requirements** 
   - Recommended configuration: Intel core i9 or i7 processor with 8 cores, 32 GB RAM
   - For development purpose, we use i7 processor with 12 cores and 32 GB RAM.
- **Operating system** : [Ubuntu 16.04.5](http://releases.ubuntu.com/16.04/)


## 3. Nvidia Jetson-TX2
-  **Hardware requirements** 
   - Jetson-Tx2 Developer Kit and peripherals (monitor, USB hub, mouse, and keyboard). 
- **Operating system** : A customized version of Ubuntu 16.04. More details in the *Installation and System Setup section*.
- **Recommended vendor**   
  - Jetson-Tx2 Developer Kit: [Available on Amazon from Nvidia](https://www.amazon.com/NVIDIA-Jetson-TX2-Development-Kit/dp/B06XPFH939).
  - Peripherals (monitor): The development kit supports HDMI. Monitor or TV (any size will work) with a HDMI input. We use ASUS monitor available [here](https://www.amazon.com/MX279H-27-Inch-1920x1080-ICEpower-Frameless/dp/B00B17C5KO/ref=sr_1_4?s=electronics&ie=UTF8&qid=1543351305&sr=1-4&keywords=asus+hdmi+monitor).
  - Peripherals (mouse, and keyboard): Connecting mouse and keyboard require a USB hub. We use USB hub available [here](https://www.amazon.com/Recbot-Indivadual-Extension-Plug-Play-Compatible/dp/B07F8L8V94/ref=sr_1_1_sspa?s=electronics&ie=UTF8&qid=1542308924&sr=1-1-spons&keywords=Recbot+USB+3.0+Hub&psc=1).


## 4. Google Vision Kit
-  **Hardware requirements** 
   - Google Vision Kit and peripherals (Android Smartphone and a separate computer). 
- **Operating system** : A customized version of Raspbian. More details in the *Installation and System Setup section*.
- **Recommended vendor** 
  - Google Vision Kit: [Available from Target](https://www.target.com/p/-/A-53417081)
  - Peripherals : Android Smartphone and a separate computer (Windows, Mac, or Linux computer) is needed to configure Google Vision Kit.


## 5. Smartphone
- Any Android smartphone can be used.
- **Recommended vendor**: [We use Samsung Galaxy S7](https://www.amazon.com/Samsung-Galaxy-S7-Unlocked-Smartphone/dp/B01CJSF8IO).
<br/>
<br/>
We are working on adding new edge devices.

---
---

# Installation and System Setup
In order to emulate the demo surveillance scenario, we will setup the below system. The installation steps are listed separately for each section.

## 1. **Host-1 (AirSim machine)**
  - Installation and system setup steps: [Available here](https://github.com/nesl/Heliot/blob/master/sensor/AirSim/Readme.md)

## 2. **Host-2 (Mininet machine)**
  - Installation and system setup steps: [Available here](https://github.com/nesl/Heliot/blob/master/network/Mininet/Readme.md)

## 3. **Nvidia Jetson-TX2**
  - Installation and system setup steps: [Available here](https://github.com/nesl/Heliot/tree/master/computation/Jetson).

## 4. **Google Vision Kit**:
  - Installation and system setup steps: [Available here](https://github.com/nesl/Heliot/blob/master/sensor/RaspberryPi/Readme.md)

## 5. **Smartphone**:
- Installation and system setup steps: To Add here.

---
---

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
<!-- 
0. Hardware
- General purpose server with Ubuntu Linux 16.04 LTS
- Recommended system requirements:
```
2 GHz dual core processor or better
2 GB system memory
5 GB of free hard drive space
Internet access
```
-->

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

2. Install ilp solvers and python packages
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
cd placethings
vim config_ddflow_demo/task_data.json

# change the ip addresses and to the correct ip addresses
172.17.51.1:18900 => the corresponding IP and port of the actuator (the display server in section 5)
172.17.49.60:18800 => the corresponding IP and port of Jetson-Tx2
```

5. run demo case
  - run the demo case
```
python main.py -tc test_ddflow_demo.Test -c config_ddflow_demo

sample output:
...
2018-11-27 17:00:38,509 |[INFO] start: start mininet.
2018-11-27 17:00:38,510 |[INFO] start: *** Starting network
...
2018-11-27 17:02:51,480 |[INFO] test: === running scenario: initial deployment ===
2018-11-27 17:02:51,481 |[INFO] start_workers: run all workers
2018-11-27 17:02:51,481 |[INFO] run_worker: run worker on CAMERA.0
2018-11-27 17:02:51,482 |[INFO] run_cmd: send command to CAMERA.0(h0): cd /opt/github/placethings && python main_entity.py run_task -n task_camera -en task_forward -a 172.18.0.2:18800 -ra 10.0.0.102:18800 &> /dev/null &
2018-11-27 17:02:51,495 |[INFO] run_cmd: output: 
2018-11-27 17:02:51,495 |[INFO] run_worker: run worker on CONTROLLER.0
2018-11-27 17:02:51,495 |[INFO] run_cmd: send command to CONTROLLER.0(h1): cd /opt/github/placethings && python main_entity.py run_task -n task_alert -en task_forward -a 10.0.0.101:18800 -ra 172.17.51.1:18900 &> /dev/null &
2018-11-27 17:02:51,509 |[INFO] run_cmd: output: 
2018-11-27 17:02:51,509 |[INFO] run_worker: run worker on P3_2XLARGE.0
2018-11-27 17:02:51,509 |[INFO] run_cmd: send command to P3_2XLARGE.0(h2): cd /opt/github/placethings && python main_entity.py run_task -n task_findObj -en task_findObj -a 10.0.0.102:18800 -ra 10.0.0.101:18800 -al offload 172.17.49.60:18800 &> /dev/null &
2018-11-27 17:02:51,517 |[INFO] run_cmd: output: 
press any key to end test
```
  - run the data forwarder so that we can send data into mininet
```
python main_entity.py run_task -n forward -en task_forward -a MININET_SERVER_IP:MININET_SERVER_PORT -ra CAMERA_IP:CAMERA_PORT
```
    * MININET_SERVER_IP:MININET_SERVER_PORT is the server ip and port you selected to run the script.
    * CAMERA_IP:CAMERA_PORT can be found in the output log, for example in this log we have CAMERA running at 172.18.0.2:18800.
```
2018-11-27 17:02:51,482 |[INFO] run_cmd: send command to CAMERA.0(h0): cd /opt/github/placethings && python main_entity.py run_task -n task_camera -en task_forward -a 172.18.0.2:18800 -ra 10.0.0.102:18800 &> /dev/null &
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
<!-- 
0. Hardware
- Smartphone with Android system
- General purpose server with any Linux-like operating systems (e.g. Ubuntu or Mac), and a public IP that accessible by your Smartphone
```
Recommended system requirements for the general purpose server:
2 GHz dual core processor or better
2 GB system memory
5 GB of free hard drive space
Internet access
```
-->

1. Install python packages
```
$ pip install --upgrade pip==9.0.1
$ sudo pip install msgpack-rpc-python future
```

2. get script from our development branch
```
wget https://raw.githubusercontent.com/kumokay/placethings/master/config_ddflow_demo/sample_display_server.py
wget https://raw.githubusercontent.com/kumokay/placethings/master/config_ddflow_demo/sample_flask_server.py
```

3. run the actuator (display server)
```
python sample_display_server.py DISPLAY_SERVER_IP:DISPLAY_SERVER_PORT
# e.g. python sample_display_server.py 172.17.51.1:18900
```

4. run the web server which gets result from the display server and shows the alert on a web page
```
python sample_flask_server.py WEB_SERVER_IP:WEB_SERVER_PORT DISPLAY_SERVER_IP:DISPLAY_SERVER_PORT
# e.g. python sample_display_server.py 172.17.51.1:7788 172.17.51.1:18900
```

5. use any web browser to open a webpage at WEB_SERVER_IP:WEB_SERVER_PORT with auto-refresh enabled. you should be able to see the result once the whole system starts running.
