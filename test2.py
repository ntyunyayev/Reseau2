from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class MyTopology(IPTopo):

    def build(self, *args, **kwargs):

        PAR_ipv4 = "162.76.1."

        r1 = self.addRouter("r1", lo_addresses=["2042:1::1/64","10.1.0.1/32"])
        r2 = self.addRouter("r2", lo_addresses=["2042:2::1/64","10.2.0.1/32"])
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")

        lr1r2 = self.addLink(r1, r2)
        lr1r2[r1].addParams(ip=("2042:12::1/64","10.12.0.1/30"))
        lr1r2[r2].addParams(ip=("2042:12::2/64","10.12.0.2/30"))

        lr1h1 = self.addLink(r1, h1)
        lr1h1[r1].addParams(ip=("2042:1a::1/64","10.51.0.1/30"))
        lr1h1[h1].addParams(ip=("2042:1a::a/64","10.51.0.2/30"))

        lr2h2 = self.addLink(r2, h2)
        lr2h2[r2].addParams(ip=("2042:2b::2/64","10.62.0.1/30"))
        lr2h2[h2].addParams(ip=("2042:2b::b/64","10.62.0.2/30"))

        super().build(*args, **kwargs)

net = IPNet(topo=MyTopology(), allocate_IPs=False)  # Disable IP auto-allocation
try:
    net.start()
    IPCLI(net)
finally:
    net.stop()