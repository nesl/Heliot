# Creating the Device Definitions File


import json


Device_1 = {
  "id" : "1",
  "type" : "AirSim",
  #"name": "AirSim Server",
  "ip": "172.17.49.168",
  #"comments": "AirSim Server is used to provide virtual sensor data from the virtual environment"
}

Device_2 = {
  "id" : "2",
  "type" : "Mininet",
  #"name": "Mininet Server",
  "ip": "172.17.49.168",
  #"comments": "Mininet Server creates a realistic virtual network between devices"
}

Device_3 = {
  "id" : "3",
  "type" : "EdgeDevice",
  #"name": "Nvidia Jetson TX2",
  "ip": "172.17.49.168",
  #"comments": "Nvidia Jetson TX2 is a edge device with local accelerator"
}

Device_4 ={
  "id" : "4",
  "type" : "EdgeDevice",
  #"name": "Google Vision Kit",
  "ip": "172.17.49.168",
  #"comments": "Google Vision Kit is a edge device with local accelerator and camera"
}


Devices = []
Devices.append(Device_1)
Devices.append(Device_2)
Devices.append(Device_3)
Devices.append(Device_4)


#y = str(Devices)

devices_json = json.dumps(Devices,"Devices",indent=1, sort_keys=False)

outputfilename = "device_testbed.json"


with open(outputfilename, 'wb') as outfile:
    outfile.write(devices_json.encode())
    outfile.close()
