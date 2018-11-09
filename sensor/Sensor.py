import random

"""
The functionality of this class depends on the type of sensor and on the type of device
"""

class Sensor:

    # Initializer
    def __init__(self, sensorType, deviceType):
        self.sensorType = sensorType
        self.deviceType = deviceType

    def getData(self):
        return random.randint(1,101)

    def getSensorType(self):
        return self.sensorType

    def getDeviceType(self):
        return self.deviceType

    def getInfo(self):
        return [self.getSensorType(),self.getDeviceType()]
