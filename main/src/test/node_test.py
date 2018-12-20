import sys
sys.path.append('../')


from core.node import *



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
sensor_1 = get_sensor()
os_1 = get_os()

n1 = node('server')

# Adding computes
n1.add_compute(compute_1)
n1.add_compute(compute_2)
# Adding memory
n1.add_memory(memory_1)
# Adding sensors
n1.add_sensor(sensor_1)
# Assing OS
n1.add_os(os_1)

type, attributes= n1.get_info()

print('Node 1 attributes')
print(type,attributes)
#print(attributes['_memory'].get_info())


# Creating an empty device
n2 = node('server')
type, attributes= n2.get_info()

print('Node 2 attributes')
print(type,attributes)
