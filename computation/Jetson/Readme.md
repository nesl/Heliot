# Nvidia Jetson-TX2 as Edge Server
[Jetson-Tx2 Developer Kit](https://developer.nvidia.com/embedded/buy/jetson-tx2-devkit) supports a Linux development environment. 

![Developer Kit](https://github.com/nesl/Heliot/blob/master/docs/images/Tx_2_dev_kit.png)

The following steps installs operating system and setup the Machine learning environment for Tensorflow. Our final goal is to run ML inference using pretrained models in Tensorflow on TX2 and add it as an edge device in Heliot framework 

## 1. Installing the operating system
The instructions to install operating system on TX-2 are available officially from Nvidia [here](https://developer.download.nvidia.com/embedded/L4T/r28_Release_v2.0/GA/Docs/Jetson_TX1_and_TX2_Developer_Kits_User_Guide.pdf) in user guide.
Some of the important points to note:
1. JetPack is installed on host OS with ubuntu 16.04. Host OS machine is connected to TX-2 using USB cable.
2. Use of Nvidia JetPack ver 3.3 is recommended which automates the installation of development environment. The instructions of using JetPack are available on page 8 of the user guide. JetPack will install OS image, CUDA, TensorRT and cuDNN library.  JetPack should have internet access inorder to install these libraries automatically using JetPack.

## 2. Setting up the development environment
1. Clone the github repo is not done already on Jetson-Tx2.
```
git clone https://github.com/nesl/Heliot.git
```

2. In the folder *Heliot/computation/Jetson/*   run. 
``` bash
bash Setup.sh
```

## 3. Testing the Installation
