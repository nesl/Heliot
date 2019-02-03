import sys

sys.path.append('../../')


from testbed import *

def get_connection(ip='', username='', password=''):
    con = connection('_ssh')
    con.add_attribute('_ip',ip)
    con.add_attribute('_username',username)
    con.add_attribute('_password',password)
    return con

def get_memory(size):
    m = memory('ram')
    m.add_attribute('size',size)
    return m

mem_32GB = get_memory(3.2e10) # 32 GB RAM
cpu_compute =  compute('cpu')# Just adding CPU without specifying number of cores


#mininet_server

mininet_server = device(id='device_mininet',type='_mininet_server')
mininet_server.add_compute(cpu_compute)
mininet_server.add_memory(mem_32GB)
mininet_server.add_os(osHeliot('_ubuntu'))
mininet_server.add_connection(get_connection('172.17.15.21','xx', 'xx'))
