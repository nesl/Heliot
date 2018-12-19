import sys
sys.path.append('../')


from core.compute import compute

type='cpu'

attributes = {
   'no_of_cores':8
}

c1 = compute(type,attributes)
print(c1)
