from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Controller, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI

class SDNTopo(Topo):
    def build(self):
        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Add links
        self.addLink(h1, s1, cls=TCLink, bw=10)
        self.addLink(h2, s1, cls=TCLink, bw=10)
        self.addLink(h3, s2, cls=TCLink, bw=10)
        self.addLink(s1, s2, cls=TCLink, bw=10)

def run():
    # Create Topology
    topo = SDNTopo()

    # Create Mininet with cleanup
    net = Mininet(topo=topo, link=TCLink, controller=None, cleanup=True)

    # Add remote controller
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Connect each switch to the controller
    for switch in net.switches:
        switch.start([c0])

    # Build network
    net.build()

    # Start controller
    c0.start()

    # Add flow entries to prioritize TCP traffic
    s1 = net.get('s1')
    s2 = net.get('s2')

    # Set OpenFlow rules to prioritize TCP traffic
    s1.cmd('ovs-ofctl add-flow s1 "priority=65535,ip,nw_proto=6,actions=output:2"')  # Send TCP traffic to port 2 (s2)
    s2.cmd('ovs-ofctl add-flow s2 "priority=65535,ip,nw_proto=6,actions=output:1"')  # Send TCP traffic to port 1 (s1)

    # Run the Mininet CLI
    CLI(net)

    # Stop Mininet
    net.stop()

if __name__ == '__main__':
    run()
