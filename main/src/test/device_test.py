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
    type='cpu'

    attributes = {
       'no_of_cores':8
    }
    compute_1 = compute(type)

    type='gpu'

    attributes = {
    }
    compute_2 = compute(type)

    return compute_1,compute_2

def get_memory():
    type='ram'

    attributes = {
       'size':5.12e8
    }

    m1 = memory(type,attributes)
    return m1

def get_connection():
    type='ssh'

    attributes = {
       'ip':'172.17.49.60',
       'username':'root',
       'password':'pwd'
    }

    con1 = connection(type,attributes)
    return con1

def get_sensor():
    type='camera'

    attributes = {
       'frame_rate':30
    }

    camera = sensor(type,attributes)
    return camera


def get_os():
    type='ubuntu'

    attributes = {
       'version':'16.4'
    }

    os_1 = os(type,attributes)
    return os_1

compute_1, compute_2 = get_compute()

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

#d1.add_sensor('sensor_1')


# Assing OS
d1.add_os(os_1)

type, attributes= d1.get_info()

print(attributes)
