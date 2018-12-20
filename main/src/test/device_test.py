import sys
sys.path.append('../')


from core.device import device
from core.compute import compute
from core.memory import memory
import json



##define compute
def get_compute():
    type='cpu'

    attributes = {
       'no_of_cores':8
    }
    compute_1 = compute(type,attributes)

    type='gpu'

    attributes = {
    }
    compute_2 = compute(type,attributes)

    return compute_1,compute_2

def get_memory():
    type='ram'

    attributes = {
       'size':5.12e8
    }

    m1 = memory(type,attributes)
    return m1


compute_1, compute_2 = get_compute()

memory_1 = get_memory()

attributes = {

'compute':[compute_1,compute_2],
'memory': memory_1

}

d1 = device('server')

# Adding computes
d1.add_compute(compute_1)
d1.add_compute(compute_2)

# Adding memory
d1.add_memory(memory_1)


type, attributes= d1.get_info()

print(attributes)
