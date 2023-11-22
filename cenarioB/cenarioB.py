from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Host, Switch
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel


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

        # Connecting switches
        self.addLink(s1, s2, cls=TCLink, bw=10)

def run():
    # Create Topology
    topo = SDNTopo()

    # Create Mininet with cleanup
    # net = Mininet(topo=topo)
    # Create Mininet with OVSSwitch and RemoteController
    net = Mininet(topo=topo, switch=OVSSwitch, controller=RemoteController, link=TCLink)
    #   net.linkDelay('s1', 's2', '10ms', '5ms')

    # Connect each switch to the controller
    for switch in net.switches:
        switch.start([])  # Start without a default controller

    # Start controller
    net.controllers[0].start()

    # Add flow entry to prioritize TCP traffic
    s1 = net.get('s1')
    s2 = net.get('s2')
    #s1.cmd('ovs-ofctl add-flow s1 "priority=65535,ip,nw_proto=6,actions=output:2"')  # Send TCP traffic to port 2 (s2)


    # Set OpenFlow rules to prioritize TCP traffic
    s1.cmd('ovs-ofctl add-flow s1 "priority=65535,ip,nw_proto=6,actions=output:2"')  # Send TCP traffic to port 2 (s2)
    s2.cmd('ovs-ofctl add-flow s2 "priority=65535,ip,nw_proto=6,actions=output:1"')  # Send TCP traffic to port 1 (s1)
    
    # h2 = net.get('h2')
    # h2.cmd('iperf -s')
    # h1 = net.get('h1')
    # h1.cmd('iperf -c 10.0.0.2 -t 10 -b 10M')
    # h3 = net.get('h3')
    # h3.cmd('iperf -c 10.0.0.2 -t 10 -b 10M')
    
    
    # Start network
    net.start()

    # Run the Mininet CLI
    CLI(net)

    # Stop Mininet
    net.stop()

if __name__ == '__main__':
    run()
