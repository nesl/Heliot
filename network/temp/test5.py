from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI

# The build() method is expected to do this:
# pylint: disable=arguments-differ

class IobT( Topo ):
    "Topology for the IobT"
    def build(self):
        # Build topology
        self.createTopo()

    def createTopo(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')
        self.addLink( h1, s1 )
        self.addLink( h2, s1 )


topo = IobT()
net = Mininet( topo)
net.addNAT().configDefault()
net.start()
CLI( net )
# Shut down NAT
net.stop()
