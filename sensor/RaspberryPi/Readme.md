# Google Vision Kit as Camera Sensor

### System: [Google Vision Kit](https://aiyprojects.withgoogle.com/vision/) 
The important components of Google Vision Kit are *Raspberry Pi Zero, Vision Bonnet and Raspberry Pi Camera*.

## 1. Setting up Vision Kit and installing the operating system 
- The instructions to assemble and connecting to Vision Kit are available [here](https://aiyprojects.withgoogle.com/vision/).
- Vision Kit comes with pre-installed system image.

## 2. Set up environment
1. Clone the github repo is not done already on Vision Kit.
```
git clone https://github.com/nesl/Heliot.git
```
2. In the folder *Heliot/sensor/RaspberryPi/*   run. 
``` bash
bash Setup.sh
```

## 3. Using as Camera Sensor
In the folder *Heliot/sensor/RaspberryPi/*   run.
<br/> 
Note: add details to update the ip of consumer of images.
``` bash
python main.py 
```
