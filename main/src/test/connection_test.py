import sys
sys.path.append('../')


from core.connection import connection

type='ssh'

attributes = {
   'ip':'172.17.49.60',
   'username':'root',
   'password':'pwd'
}

con1 = connection(type,attributes)
print(con1)
