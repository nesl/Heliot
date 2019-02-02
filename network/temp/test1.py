from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0') #docker_ip=172.18.0.1


info('*** Adding docker containers\n')
leftHost = net.addHost('leftHost', ip='10.0.0.21')#docker_ip=172.18.0.2
rightHost = net.addHost('rightHost', ip='10.0.0.22')#docker_ip=172.18.0.3

info('*** Adding switches\n')
s1 = net.addSwitch('s1')


info('*** Creating links\n')
net.addLink(leftHost, s1)
net.addLink(rightHost, s1)

info('*** Starting network\n')
net.start()


print "Left host commands"
print "*"*100
print leftHost.cmd('ping -c1 %s' % rightHost.IP())
print leftHost.cmd('python3 gvt.py ')

print "Right host commands"
print "*"*100
print rightHost.cmd('ping -c1 %s' % leftHost.IP())


info('*** Stopping network')
net.stop()
