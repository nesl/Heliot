"""
 Goals is to create three hosts connected to the switch
 1) Camera host: To receive the camera Images.
 2) TX2 host: To interact with the Jetson-Tx2.
 3) Actuator host to interact with the display process (RPC code) to display the results.
"""


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
# 19000 is port exposed to public from docker
# 20000 is the internal port of the docker listening on 19000
cam = net.addDocker('cam', ip='10.0.0.101', dimage="sandynesl/heliot:1", ports=[19000], port_bindings={19000: 20000})#docker_ip=172.18.0.2

tx2 = net.addDocker('tx2', ip='10.0.0.102', dimage="sandynesl/heliot:1")#docker_ip=172.18.0.3
act = net.addDocker('act', ip='10.0.0.103', dimage="sandynesl/heliot:1")#docker_ip=172.18.0.4

info('*** Adding switches\n')
s1 = net.addSwitch('s1')


info('*** Creating links\n')
net.addLink(cam, s1)
net.addLink(tx2, s1)
net.addLink(act, s1)

info('*** Starting network\n')
net.start()


info('*** Testing connectivity\n')
net.ping([cam, tx2])


info('*** Running CLI\n')
CLI(net)

# Now run the individual container code
# Code on TX2 Container: TX address is 172.17.49.168:18801
# tx2 cd /opt/github/placethings && python main_entity.py run_task -n task_findObj -en task_findObj -a 10.0.0.102:18800 -ra 10.0.0.101:18800 -al offload 172.17.49.168:18801 &> /dev/null &

# Code on Camera Container:
# cam cd /opt/github/placethings && python main_entity.py run_task -n task_camera -en task_forward -a 172.18.0.2:18800 -ra 10.0.0.102:18800 &> /dev/null &

# Code on Actuator: to forward to the display server
# act cd /opt/github/placethings && python main_entity.py run_task -n task_alert -en task_forward -a 10.0.0.101:18800 -ra 172.17.49.168:18900 &> /dev/null &

# We need to run the data forwarder on the Mininet machine
# python main_entity.py run_task -n forward -en task_forward -a 172.17.49.168:18800 -ra 172.18.0.2:18800



info('*** Stopping network')
net.stop()
