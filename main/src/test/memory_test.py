import sys
sys.path.append('../')


from core.memory import memory

type='ram'

attributes = {
   'size':5.12e8
}

m1 = memory(type,attributes)
print(m1)
