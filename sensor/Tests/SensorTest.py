#Making one module visible to another
import sys
sys.path.append('../')

from Sensor import Sensor


#s1 = Sensor("Camera","Pi")
s1 = Sensor()
print("Data is:",s1.getData())
print("Sensor is:",s1)
