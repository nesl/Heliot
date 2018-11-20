# Heliot: Hybrid Emulation of Learning Enabled IoT systems


**Heliot** is a framework to emulate different IoT scenarios. An Iot scenario in Heliot consists of sensors (both real and virtual), compute resources (cloud, cloudlet, edge devices, containers etc) running computation and a dynamic network topology.  Heliot simplifies to study the application performance in presence of heterogeneous compute resources, sensors, dynamic network characteristics,and compute parition and placement algorithms. Heliot is in active development. 

<br />

To better understand the Heliot, let us consider a demo IoT scenario of surveillance as follows.

![Demo Surveillance Scenario](https://github.com/nesl/Heliot/blob/master/docs/images/Demo_Arch_1.png)

This scenario consists of the following components:
- Object detection inference of detecting Cars and Person from images using Neural Network.
- Sensors (**Google Vision Kit** and **Drone** in Airsim having Camera).
- Compute resources (Google Vision Kit, Virtual Container, Nvidia Jetson TX-2).
- Network emulation using **Mininet**.
- User **Smartphone** to deliver the notification.

<br />

# Installation
In order to emulate the demo surveillance scenario, we will setup the below system.

- **Nvidia Jetson-TX2**: [Nvidia Jetson-TX2](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems-dev-kits-modules/) will act as an edge server having GPU (local accelerator). 
  - Installation Steps: [Available here](https://github.com/nesl/Heliot/tree/master/computation/Jetson).

- **Windows machine running Airsim**: Our goal is to setup a drone in AirSim having camera sensor. 
  - Skip this step, if virtual drone having camera as sensor is not needed.
  - Installation Steps: Add Installation Steps.
