# Heliot: Hybrid Emulation of Learning Enabled IoT systems


**Heliot** is a framework to emulate different IoT scenarios. An Iot scenario in Heliot consists of sensors (both real and virtual), compute resources (cloud, cloudlet, edge devices, containers etc) running computation and a dynamic network topology.  Heliot simplifies to study the application performance in presence of heterogeneous compute resources, sensors, dynamic network characteristics,and compute partition and placement algorithms. Heliot is in active development. 

<br />
<br />

**[Heliot received the best demo award at IoTDI 2019](https://conferences.computer.org/iotDI/prev/2019/).**

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
We are actively working on adding new edge devices, support and documentation.

---
---

# Installation and System Setup
In order to emulate the demo surveillance scenario, we will setup the below system. The installation steps are listed separately for each section.

## 1. **Host-1 (AirSim machine)**
  - Installation and system setup steps: [Available here](https://github.com/nesl/Heliot/blob/master/sensor/AirSim/Readme.md)

## 2. **Host-2 (Mininet machine)**
  - Installation and system setup steps: [Available here](https://github.com/nesl/Heliot/blob/master/network/README.md)

## 3. **Nvidia Jetson-TX2**
  - Installation and system setup steps: [Available here](https://github.com/nesl/Heliot/tree/master/computation/Jetson).

## 4. **Google Vision Kit**:
  - Installation and system setup steps: [Available here](https://github.com/nesl/Heliot/blob/master/sensor/RaspberryPi/Readme.md)

## 5. **Smartphone**:
- Installation and system setup steps: [Available here](https://github.com/nesl/Heliot/blob/master/UserDevice/smartphone/Readme.md)

---
---

# Running Demo Scenario

<!--Currently Heliot is still under development. -->
 Heliot is in active development.
Please follow the installation and system set up steps listed above. 

## 1. Inference on Jetson-Tx2
In the folder Heliot/computation/Jetson/ run.
```
python3 main.py JETSON_PORT_NUM
```
PORT_NUM can be: 18800
<br/>
Wait until you see, the below output in the terminal before running any sensor code or the test code.
```
Available for Inference now
```

<br/>
To verify, that Jetson-Tx2 is running as inference server run.

```
python3 test.py JETSON_PORT_NUM
```
 
## 2. Running Network Emulator

#### 0. get source code and install required packages by following the steps described [here](https://github.com/nesl/Heliot/blob/master/network/README.md)

#### 1. modify the config file and change the ip addresses and to the correct ip addresses
```
cd placethings
vim config_ddflow_demo/task_data.json
```
- 172.17.51.1:18900 => the corresponding IP and port of the actuator, which would be the DISPLAY_SERVER_IP:DISPLAY_SERVER_PORT described in [UserDevice/smartphone section](https://github.com/nesl/Heliot/blob/master/UserDevice/smartphone/Readme.md#3-run-the-actuator-display-server) in this demo
- 172.17.49.60:18800 => the corresponding IP and port of Jetson-Tx2

#### 2. run the demo case with sudo (because mininet requires root access to simulate the network)
```
# clean up mininet objects (if any)
sudo mn -c

# run the demo case
sudo python main.py demo -tc test_ddflow_demo.Test -c config_ddflow_demo

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
#### 3. run the data forwarder so that we can send data into mininet
    - MININET_SERVER_IP:MININET_SERVER_PORT is the server ip and port you selected to run the script.
    - CAMERA_IP:CAMERA_PORT can be found in the output log, for example in the log above, CAMERA is running at 172.18.0.2:18800.
```
partial output log:
...
2018-11-27 17:02:51,482 |[INFO] run_cmd: send command to CAMERA.0(h0): cd /opt/github/placethings && python main_entity.py run_task -n task_camera -en task_forward -a 172.18.0.2:18800 -ra 10.0.0.102:18800 &> /dev/null &
...

python main_entity.py run_task -n forward -en task_forward -a MININET_SERVER_IP:MININET_SERVER_PORT -ra CAMERA_IP:CAMERA_PORT
```

## 3. Google Vision Kit as Camera Sensor

In the folder *Heliot/sensor/RaspberryPi/*   run.
<br/> 
Note: add details to update the ip of consumer of images.
``` bash
python main.py MININET_SERVER_IP MININET_SERVER_PORT
```

## 4. Virtual drone in AirSim as Camera Sensor

0. get source code and install required packages by following the steps described [here](https://github.com/nesl/Heliot/blob/master/sensor/AirSim/Readme.md)

1. run the python client to control the drone
    - MININET_MACHINE_IP:MININET_MACHINE_PORT is the IP and port you used for your data forwarder in [section 3](https://github.com/nesl/Heliot/blob/master/README.md#3-run-the-data-forwarder-so-that-we-can-send-data-into-mininet)
```
cd airsim_python_client\PythonClient\multirotor
python _multi_drone_threading.py MININET_MACHINE_IP:MININET_MACHINE_PORT
```

## 5. User Smartphone for notification

1. Setup web server as mentioned in [installation steps](https://github.com/nesl/Heliot/blob/master/UserDevice/smartphone/Readme.md).

2. We are actively working on developing an Android App. Currently, we refresh the web address hosted by the
web server which is setup in the previous step on the user smartphone.

5. Use any web browser in the Smartphone to open a webpage at http://WEB_SERVER_IP:WEB_SERVER_PORT with auto-refresh enabled. 
<br/>

Another easy way is to use auto refresh Android application. We recommend using [Auto refresh web page utility](https://play.google.com/store/apps/details?id=com.murgoo.autowebpagerefresh). In the settings tab add http://WEB_SERVER_IP:WEB_SERVER_PORT 

<br/>
you should be able to see the result once the whole system starts running.


## Scenario-2: Computation Split using Deep RL
- Details are [here](https://github.com/nesl/Heliot/tree/master/Scenario-2).

