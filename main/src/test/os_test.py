import sys
sys.path.append('../')


from core.os import os

type='ubuntu'

attributes = {
   'version':'16.4'
}

os = os(type,attributes)
print(os)
