from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class multipleSwitch( Topo ):

    def __init__( self ):
        #init topo
        Topo.__init__(self)

        switches = []

        #init switches
        for i in range(4):
            switch = self.addSwitch('s%s' %(i+1))
            switches.append(switch)

        #init links for switch cluster
        self.addLink(switches[0],switches[1],bw=1000)
        self.addLink(switches[1],switches[3],bw=1000)
        self.addLink(switches[0],switches[2],bw=1000)
        self.addLink(switches[2],switches[3],bw=1000)


        self.addLink(switches[0],switches[3],bw=100)
        self.addLink(switches[1],switches[2],bw=100)

        #create hosts
        hosts = []
        for i in range(4):
            host = self.addHost('h%s' % (i+1))
            hosts.append(host)
        
        #create links towards hosts
        self.addLink(hosts[0],switches[0],bw=100)
        self.addLink(hosts[1],switches[2],bw=100)
        self.addLink(hosts[2],switches[1],bw=100)
        self.addLink(hosts[3],switches[3],bw=100)


topos = {'multipleSwitch':multipleSwitch}