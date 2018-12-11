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
camera_host = net.addDocker('Cam', ip='10.0.0.21', dimage="kumokay/ubuntu_wifi:v6")#docker_ip=172.18.0.2
Tx2_host = net.addDocker('Tx2', ip='10.0.0.102', dimage="kumokay/ubuntu_wifi:v6")#docker_ip=172.18.0.3
Actuator_host = net.addDocker('Act', ip='10.0.0.101', dimage="kumokay/ubuntu_wifi:v6")#docker_ip=172.18.0.4

info('*** Adding switches\n')
s1 = net.addSwitch('s1')


info('*** Creating links\n')
net.addLink(camera_host, s1)
net.addLink(Tx2_host, s1)
net.addLink(Actuator_host, s1)

info('*** Starting network\n')
net.start()


info('*** Testing connectivity\n')
net.ping([camera_host, Tx2_host])



info('*** Running CLI\n')
CLI(net)

# Now run the individual container code
# Code on TX2 Container: TX address is 172.17.49.168:18801
# Tx2 cd /opt/github/placethings && python main_entity.py run_task -n task_findObj -en task_findObj -a 10.0.0.102:18800 -ra 10.0.0.101:18800 -al offload 172.17.49.168:18801 &> /dev/null &

# Code on Camera Container:
# Cam cd /opt/github/placethings && python main_entity.py run_task -n task_camera -en task_forward -a 172.18.0.2:18800 -ra 10.0.0.102:18800 &> /dev/null &

# Code on Actuator: to forward to the display server
# Act cd /opt/github/placethings && python main_entity.py run_task -n task_alert -en task_forward -a 10.0.0.101:18800 -ra 172.17.49.168:18900 &> /dev/null &

# We need to run the data forwarder on the Mininet machine
# python main_entity.py run_task -n forward -en task_forward -a 172.17.49.168:18800 -ra 172.18.0.2:18800



info('*** Stopping network')
net.stop()
