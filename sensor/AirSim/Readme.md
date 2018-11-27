# AirSim

## Goal: Setup up [AirSim simulator](https://github.com/Microsoft/AirSim) in a Windows machine where virtual drone acts as image sensor.

### System: Machine with Windows 10.
Recommended System: Machine with 32 GB RAM and [NVIDIA TitanX](https://www.nvidia.com/en-us/geforce/products/10series/titan-x-pascal/) GPU. Typical AirSim workload require GPUs with at least 4GB of RAM. 

## 1. Setting up the Machine
1. **Installing windows 10** on the machine. Many online resources are available. A complete step-by-step guide is [here](https://www.howtogeek.com/197559/how-to-install-windows-10-on-your-pc/)
2. **Nvidia GPU Drivers** need to be installed. The steps are available [here](https://nvidia.custhelp.com/app/answers/detail/a_id/2900/~/installing-nvidia-display-drivers-under-windows-7%2C-windows-8%2C-or-windows-10).

## 2. AirSim
1. Use precompiled binaries: Download the precompiled binary for [AirSimNH](https://github.com/Microsoft/AirSim/releases/download/v1.2.1/AirSimNH.zip). AirSimNH is small urban neighbourhood block. 
2. Extract it somewhere and run the run.bat to verify the AirSim simulator works.

## 3. Setting up development environment
1. Set up python by following the steps [here](https://docs.python.org/3/using/windows.html).
2. Install the packages. Note: Add instructions.

## 4. Testing drone locally
1. Clone the github repo is not done already on the machine.
```bash
git clone https://github.com/nesl/Heliot.git
```
2. Running drone on predefined trajectory
<br/>
- Move the settings.json file to the folder location.
<br/>
- In the folder *Heliot/sensor/AirSim*   run. 

``` bash
python3 hello_drone.py
```
