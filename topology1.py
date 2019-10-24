from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class SingleSwitchTopo( Topo ):

	def __init__( self ):
		#init topo
		Topo.__init__(self)

		#add switches, hosts and links
		switch = self.addSwitch('s1')
		for i in range(3):
			host = self.addHost('h%s' % (i+1))
			self.addLink(host,switch,bw=100)


topos = {'singleswitchtopo':SingleSwitchTopo}