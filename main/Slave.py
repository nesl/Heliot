
#Making one module visible to another
import sys
sys.path.append('../')


# importing the sensor module
from sensor.Sensor import Sensor

# A class which runs on any deviceself.
# Should be able to get sensor getData
# Should be able to schedule the computation
class Slave:

    # Initializer
    def __init__(self):
        pass


    def setSensor(self,sensor):
        self.sensor= sensor

    def printSensor(self):
        print('Sensor is:',self.sensor.getInfo())

    def setCompute(self,compute):
        self.compute=compute
        print(self.compute.getInfo())

    def printCompute(self):
        #pass
        info=self.compute.getInfo()
        print('*'*50)
        print('*'*50)
        print('Compute is:',info)
        print('*'*50)

    def runCompute(self):
        return self.compute.runCompute()

    def updateComputeData(self,data):
        self.compute.initData(data)
        print('updated data: ',data.shape)

    def updateComputeDataFromSensor(self):
        self.compute.initData(self.sensor.getData())
