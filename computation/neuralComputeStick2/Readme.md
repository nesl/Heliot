# Setting up OpenVINO tootkit to run inferences using Neural Compute Stick-2

## Note this code and setup also work for Neural Compute Stick-1

## 1. Install OpenVINO
Steps are available [here](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)

## 2. Downloading Model and Setting up Environment
``` bash
cd Heliot/computation/neuralComputeStick2/setup
bash setup.sh
```

## 3. Running Inference
see sample results in: Heliot/computation/neuralComputeStick2/Object_recognition.ipynb

- The numbers for Neural Compute Stick: 
  - *Total Time taken transfer model and to run Inference is: 3.96 sec*
  - *Time to run Inference is: 0.0414 sec*
 
- The numbers for Neural Compute Stick2:
  - *Total Time taken transfer model and to run Inference is: 3.85 sec*
  - *Time to run Inference is: 0.144 sec*
