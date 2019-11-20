"""
Heliot Framework abstractions are Devices, Nodes and Tasks
Devices are part of Testbed and Nodes are part of the scenario
which are mapped to Devices

Scenario definition consists of nodes which are of three types: nodes, infranode and virtual_Sensors
All of these nodes are connected using an emulated network which is created using Mininet.

net.py provides the capabilites to create a network of desired configuration as specified
in the scenario.py file.
"""

#Mininet imports
# We are using the containernet to do the job, so as to run each mininet container within
# a separate docker container
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel

#setLogLevel('info')



class netHeliot:

    def __init__(self):
        self._network=Mininet(controller=Controller)
        self._network.addController('c0')
        self._switches={}
        self._hosts={}


        #Keeping track of ip assignment
        self._ip_first = "10.0.0"
        self._ip_last = 1

    #id of the switch to add
    def add_switch(self,id=''):
        # Switch is assigned ip automatically by mininet and is not overidden

        s = self._network.addSwitch(id)
        self._switches[id]=s

    #id of the host to add
    def add_host(self,id=''):
        #ip for the host
        ip = self._ip_first+"."+str(self._ip_last)
        self._ip_last=self._ip_last+1

        h = self._network.addHost(id,ip=ip)

        self._hosts[id]=h

    #adding a mininet link between node1 and node2
    def add_link(self,node1,node2, delay="0ms"):
        self._network.addLink(node1, node2, delay=str(delay) + 'ms')

    def get_host(self, id=''):
        if id in self._hosts:
            #print "host returned"
            return self._hosts[id]
        else:
            return None

    def get_switch(self, id=''):
        if id in self._switches:
            #print "switch returned"
            return self._switches[id]
        else:
            return None


#Local testing
# net1 = netHeliot()
#
# net1.add_switch('s1')
# net1.add_host('h1')
# net1.add_host('h2')
#
# s1 = net1.get_switch('s1')
# h1 = net1.get_host('h1')
# h2 = net1.get_host('h2')
#
# net1.add_link(s1,h1)
# net1.add_link(s1,h2)
#
#
# net1._network.start()
#
# print("h1.IP():",h1.IP())
# print("h2.IP():",h2.IP())
# print("s1.IP():",s1.IP())
#
#
# print(h1.cmd('ping -c1 %s' % h2.IP()))
#
# net1._network.stop()
