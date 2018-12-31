import sys
sys.path.append('../')


from core.infranode import infranode

virtual_switch = infranode('switch')
virtual_switch.add_attribute('id','virtual_switch_0')
virtual_switch.add_attribute('description','Virtual switch used in mininet')

print(virtual_switch.get_info())
