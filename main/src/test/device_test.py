import sys
sys.path.append('../')


from core.device import device
from core.compute import compute
from core.memory import memory
from core.connection import connection
from core.sensor import sensor
from core.os import os
import json



##define compute
def get_compute():
    compute_1 = compute('cpu')
    compute_1.add_attribute('no_of_cores',8)
    compute_2 = compute('gpu')
    return compute_1,compute_2

def get_memory():
    m1 = memory('ram')
    m1.add_attribute('size',5.12e8)
    return m1

def get_connection():
    con1 = connection('ssh')
    con1.add_attribute('ip','172.17.49.60')
    con1.add_attribute('username','root')
    con1.add_attribute('password','pwd')
    return con1

def get_sensor():
    camera = sensor('camera')
    camera.add_attribute('frame_rate',30)
    return camera


def get_os():
    os_1 = os('ubuntu')
    os_1.add_attribute('version','16.04')
    return os_1

compute_1, compute_2 = get_compute()

#print(compute_2._attributes)
# print(compute_2.get_info())



memory_1 = get_memory()

connection_1 = get_connection()

sensor_1 = get_sensor()

os_1 = get_os()

d1 = device('server')

# Adding computes
d1.add_compute(compute_1)
d1.add_compute(compute_2)
# Adding memory
d1.add_memory(memory_1)
# Adding _connection
d1.add_connection(connection_1)
# Adding sensors
d1.add_sensor(sensor_1)
# Assing OS
d1.add_os(os_1)

type, attributes= d1.get_info()

print('Device 1 attributes')
#print(type,attributes)
#print(attributes['_memory'].get_info())


d2 = device('server2')
type, attributes= d2.get_info()

print('Device 2 attributes')
print(type,attributes)
