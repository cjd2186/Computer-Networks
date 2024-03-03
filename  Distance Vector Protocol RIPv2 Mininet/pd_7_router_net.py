import os

from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import Node, Controller, CPULimitedHost

class LinuxRouter(Node):     # from the Mininet library
    "A Node with IP forwarding enabled."
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        info ("Enabling forwarding on ", self)
        self.cmd("sysctl net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(LinuxRouter, self).terminate()

def Network():
    info('*** Creating a network with no nodes or links\n')
    net = Mininet(host=CPULimitedHost, link=TCLink, autoStaticArp=False)

    #Modified the router host names
    info('*** Adding hosts\n')
    r1 = net.addHost('u', cls=LinuxRouter)
    r2 = net.addHost('v', cls=LinuxRouter)
    r3 = net.addHost('x', cls=LinuxRouter)
    r4 = net.addHost('w', cls=LinuxRouter)
    r5 = net.addHost('y', cls=LinuxRouter)
    r6 = net.addHost('z', cls=LinuxRouter)
    
    #Modified the links
    info('*** Creating links\n')
    net.addLink(r1, r2, intfName1="u-i2", intfName2="v-i1")
    net.addLink(r1, r3, intfName1="u-i3", intfName2="x-i1")
    net.addLink(r1, r4, intfName1="u-i4", intfName2="w-i1")
    net.addLink(r2, r3, intfName1="v-i3", intfName2="x-i2")
    net.addLink(r2, r4, intfName1="v-i4", intfName2="w-i2")
    net.addLink(r3, r4, intfName1="x-i4", intfName2="w-i3")
    net.addLink(r3, r5, intfName1="x-i5", intfName2="y-i3")
    net.addLink(r4, r5, intfName1="w-i5", intfName2="y-i4")
    net.addLink(r4, r6, intfName1="w-i6", intfName2="z-i4")
    net.addLink(r5, r6, intfName1="y-i6", intfName2="z-i5")

    info('*** Starting network\n')
    net.start()

    info('*** Configuring interface IPs\n')
    for router in net.hosts:
        """Each link between 2 routers is in a 172.16.xy.z/24 subnet, where
            x = lower ID of the 2 routers
            y = higher ID of the 2 routers
            z = local router id
        """
        for idx, r_intf in router.intfs.items():
            local_id, peer_id = map(lambda x: x[-1], r_intf.name[1:].split("-"))
            if local_id < peer_id:
                router.setIP(f"172.16.{local_id}{peer_id}.{local_id}/24", intf=r_intf)
            else:
                router.setIP(f"172.16.{peer_id}{local_id}.{local_id}/24", intf=r_intf)

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    os.system("sudo mn -c") # Clear out the remnants of failed runs (if they exist).
    setLogLevel( 'info' )
    Network()