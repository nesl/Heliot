import random

"""
The functionality of this class depends on the type of sensor and on the type of device.
The purpose of this class:
1) Define an abstract class defining the most basic functionality which should be implemented by any
sensing class.
2) The functions are defined as below:
a)    __init__: The initializer of the class.
b) getData: This function returns the data of the sensor. At present, in this base class it returns a random integer
    between 1 and 100

"""

class Sensor:

    # Initializer
    def __init__(self, sensorType=None, deviceType=None):
        self.sensorType = str(sensorType)
        self.deviceType = str(deviceType)


    def setSensorType(self, sensorType):
        self.sensorType = sensorType

    def setDeviceType(self, sensorType):
        self.deviceType = deviceType


    # This is the main data function which every sensor should define
    def getData(self):
        return random.randint(1,100)

    def getSensorType(self):
        return self.sensorType

    def getDeviceType(self):
        return self.deviceType

    #Overloading the print sensor function.
    def __str__(self):
        return self.getSensorType()+" - "+self.getDeviceType()

    def getInfo(self):
        return [self.getSensorType(),self.getDeviceType()]
