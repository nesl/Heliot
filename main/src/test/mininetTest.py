import sys
sys.path.append('../')


from network.netHeliot import *



net1 = netHeliot()

net1.add_switch('s1')
net1.add_host('h1')
net1.add_host('h2')

s1 = net1.get_switch('s1')

h1 = net1.get_host('h1')
h2 = net1.get_host('h2')

net1.add_link(s1,h1)
net1.add_link(s1,h2)


net1._network.addNAT().configDefault()
net1._network.start()

print("h1.IP():",h1.IP())
print("h2.IP():",h2.IP())
print("s1.IP():",s1.IP())


print(h1.cmd('ping -c1 %s' % h2.IP()))

print(h1.cmd('ping -c1 www.google.com' ))

CLI(net1._network)

net1._network.stop()
