# Nvidia Jetson-TX2 as Edge Server
[Jetson-Tx2 Developer Kit](https://developer.nvidia.com/embedded/buy/jetson-tx2-devkit) supports a Linux development environment. 

![Developer Kit](https://github.com/nesl/Heliot/blob/master/docs/images/Tx_2_dev_kit.png)

The following steps installs operating system and setup the Machine learning environment for Tensorflow. Our final goal is to run ML inference using pretrained models in Tensorflow on TX2 and add it as an edge device in Heliot framework 

## 1. Installing the operating system
The instructions to install operating system on TX-2 are available officially from Nvidia [here](https://developer.download.nvidia.com/embedded/L4T/r28_Release_v2.0/GA/Docs/Jetson_TX1_and_TX2_Developer_Kits_User_Guide.pdf) in user guide.
The recommendations for easy system setup are discussed next.
1. Use of Nvidia JetPack ver 3.3 is recommended which automates the installation of development environment. The instructions of using JetPack are available on page 8 of the user guide. JetPack will install OS image, CUDA, TensorRT and cuDNN library. 
2. After downloading the file, make the file executable. 


## 2. Setting up the development environment
