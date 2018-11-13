import sys
sys.path.append('../')
import random


from Sensor import Sensor

class CameraPi(Sensor):

    # Initializer
    def __init__(self, sensorType=None, deviceType=None):
        super().__init__(sensorType, deviceType)

    # This is the main data function which every sensor should define
    def getData(self):
        return random.randint(1,100)
