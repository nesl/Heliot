from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from time import sleep
setLogLevel('info')


net = Containernet(controller=Controller)
info('Adding controller...\n')
net.addController('c0')


info('Adding hosts...\n')
node1 = net.addHost('n1', ip='10.0.0.101')
node2 = net.addHost('n2', ip='10.0.0.102')


info('Adding Switches...\n')
s1 = net.addSwitch('s1')


info('Creating Links...\n')
net.addLink(s1, node1)
net.addLink(s1, node2)


info('Starting Network...\n')
net.addNAT().configDefault()
net.start()


info('Testing connection...\n')
net.pingAll()
print (node1.IP(), node2.IP())


info('Network running... type exit to stop\n')
node2.cmd('cd /home/prince/Desktop/prince/test_1 && python3 sendPic.py receive node2 &')
sleep(1)    # Give receiver some time to initialize
node1.cmd('cd /home/prince/Desktop/prince/test_1 && python3 sendPic.py send node1 node2 &')
CLI(net)


info('Stopping Network\n')
net.stop()