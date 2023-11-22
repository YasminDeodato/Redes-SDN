from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI

class nonSDNTopology(Topo):
    def build(self):
        # Adding switches
        switch1 = self.addSwitch('s1')

        # Adding hosts
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')

        # Connecting hosts to switches
        self.addLink(host1, switch1)
        self.addLink(host2, switch1)
        self.addLink(host3, switch1)

def create_network():
    topo = nonSDNTopology()
    net = Mininet(topo=topo)
    net.start()

    # Starting Mininet CLI
    CLI(net)

    # Stopping the network upon exiting the CLI
    net.stop()

if __name__ == '__main__':
    create_network()
