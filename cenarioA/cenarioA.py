from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Host, Switch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class MyTopology(Topo):
    def build(self):
        # Adding switches
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')

        # Adding hosts
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')

        # Connecting hosts to switches with a bandwidth limit of 10 Mbps
        self.addLink(host1, switch1, cls=TCLink, bw=10)
        self.addLink(host2, switch1, cls=TCLink, bw=10)
        self.addLink(host3, switch2, cls=TCLink, bw=10)

        # Connecting switches
        self.addLink(switch1, switch2, cls=TCLink, bw=10)

def create_network():
    topo = MyTopology()
    net = Mininet(topo=topo)
    net.start()

    # Starting Mininet CLI
    CLI(net)

    # Stopping the network upon exiting the CLI
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_network()
