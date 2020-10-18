#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, RouterConfig, AF_INET6, set_rr, ebgp_session, SHARE


class SimpleBGPTopo(IPTopo):
    """
    Please read me before digging in the code of this script.

    This simple network topology tries to connect two hosts separated
    by multiple routers and ASes.

    Running this network should be straightforward:
     i./ The script must be run as root since mininet will create routers inside your own machine
         $ chmod +x main.py
         $ sudo ./main.py
    
    ii./ The network should be started. The "mininet" CLI should appear on screen
    '''
    mininet>
    '''

    To access to one of the network, execute this command "xterm <your node name>". A new
    xterm terminal will be spawned. This new terminal will run bash. This means that you
    can execute any linux command. Be careful as the terminal is run as root!!

    '''
    mininet> xterm as1_rr1
    '''

    To access to the configuration of FRRouting, you have to use telnet to connect to
    FRRouting daemons.
    A different port is used to access to every routing daemon. This small table shows
    the port associated to its default daemon:

    PORT     STATE SERVICE
    2601/tcp open  zebra   --> controls the RIB of each daemon
    2605/tcp open  bgpd    --> show information related to the configuration of BGP
    2606/tcp open  ospf6d  --> same but for OSPFv3 (OSPF for IPv6)

    For example, if you want to look for all prefixes contained in the RIB, you must execute
    this command :
    <in the xterm of your node>$ telnet localhost 2601

    A new cli interface will be shown:

    '''
    Trying ::1...
    Connected to localhost
    Escape character is '^]'.

    Hello, this is FRRouting (version v7.4).
    Copyright 1996-2005 Kunihiro Ishiguro, et al.

    User Access Verification

    Password:
    '''

    At this time, you will be prompted for a password. In ipmininet the default password is "zebra".
    Simply type it and the FRRouting CLI will be shown:

    '''
    as1_rr1>
    '''

    Type "show ipv6 route" to show all the routes contained in the RIB. You can find an example of output below
    ''''
    as1_rr1> show ipv6 route
    Codes: K - kernel route, C - connected, S - static, R - RIPng,
           O - OSPFv3, I - IS-IS, B - BGP, N - NHRP, T - Table,
           v - VNC, V - VNC-Direct, A - Babel, D - SHARP, F - PBR,
           f - OpenFabric,
           > - selected route, * - FIB route, q - queued route, r - rejected route

    B>* c1a4:4ad:c0ff:ee::/64 [20/0] via fe80::f802:bbff:fe6d:4da0, as1_rr1-eth2, weight 1, 00:50:34
    O>* cafe:babe:dead:beaf::/64 [110/2] via fe80::2c5c:4ff:fe4a:2b73, as1_rr1-eth1, weight 1, 00:50:30
    O   fc00:0:3::/48 [110/1] is directly connected, as1_rr1-eth0, weight 1, 00:50:35
    C>* fc00:0:3::/48 is directly connected, as1_rr1-eth0, 00:50:38
    O   fc00:0:4::/48 [110/1] is directly connected, as1_rr1-eth1, weight 1, 00:50:35
    C>* fc00:0:4::/48 is directly connected, as1_rr1-eth1, 00:50:38
    B   fc00:0:5::/48 [20/0] via fe80::f802:bbff:fe6d:4da0, as1_rr1-eth2, weight 1, 00:50:34
    O   fc00:0:5::/48 [110/1] is directly connected, as1_rr1-eth2, weight 1, 00:50:38
    C>* fc00:0:5::/48 is directly connected, as1_rr1-eth2, 00:50:38
    O>* fc00:0:6::/48 [110/2] via fe80::c07a:14ff:feaf:83d3, as1_rr1-eth0, weight 1,  00:50:30
    O>* fc00:0:7::/48 [110/2] via fe80::c07a:14ff:feaf:83d3, as1_rr1-eth0, weight 1, 00:50:30
    B   fc00:0:7::/48 [200/0] via fc00:0:3::1, as1_rr1-eth0, weight 1, 00:50:34
    O>* fc00:0:8::/48 [110/2] via fe80::2c5c:4ff:fe4a:2b73, as1_rr1-eth1, weight 1, 00:50:30
    O   fc00:0:9::/48 [110/1] is directly connected, lo, weight 1, 00:50:38
    C>* fc00:0:9::/48 is directly connected, lo, 00:50:39
    O>* fc00:0:a::/48 [110/2] via fe80::c07a:14ff:feaf:83d3, as1_rr1-eth0, weight 1, 00:50:30
    O>* fc00:0:b::/48 [110/3] via fe80::2c5c:4ff:fe4a:2b73, as1_rr1-eth1, weight 1, 00:50:25
      *                       via fe80::c07a:14ff:feaf:83d3, as1_rr1-eth0, weight 1, 00:50:25
    O>* fc00:0:c::/48 [110/2] via fe80::2c5c:4ff:fe4a:2b73, as1_rr1-eth1, weight 1, 00:50:30
    B>* fc00:0:d::/48 [20/0] via fe80::f802:bbff:fe6d:4da0, as1_rr1-eth2, weight 1, 00:50:34
    B>* fc00:0:e::/48 [200/0] via fc00:0:3::1, as1_rr1-eth0, weight 1, 00:50:34
    C * fe80::/64 is directly connected, as1_rr1-eth0, 00:50:38
    C * fe80::/64 is directly connected, as1_rr1-eth2, 00:50:38
    C>* fe80::/64 is directly connected, as1_rr1-eth1, 00:50:38
    '''

    Press CTRL + D to exit the session. And again to exit the xterm session.

    You can find more information on how to use the CLI of FRRouting daemons in the FRRouting DOCS:
    http://docs.frrouting.org/en/latest/

    Remember that xterm launches a root bash. You can run any executable (in ROOT!).
    If wireshark is installed on your computer, you can execute it to capture packets
    reaching interfaces of your mininet node.

    The same applies if you want to check the Linux FIB (ip addr) or the addresses attached to the node
    interfaces (ip route)

    Finally, you can find other details on how to build an ipmininet script here:
    https://ipmininet.readthedocs.io/en/latest/
    """

    # 1. Can you picture the topology described in this python script ?
    #    Draw this topology by hand before running it in ipmininet.
    # 2. This small network is faulty. Can you find the problem ?
    # 3. Propose a fix to make this network operational again
    # 4. How can you do to check the LSDB of OSPF ?
    # 5. Again use it to show details abol_PAR1_PAR2[PAR1].addParams(ip=(europe_ipv6 + "00:1201::/64"))ut the BGP sessions.
    # 6. Add a new AS (AS3) on top of this topology which will contain 4 routers, each running
    #    OSPFv3 and BGP. Add also a new host as3_h3 in a new lan taco:d0d0:i5:dead::/64 in one of the 4 routers.
    #    h1, h2 and h3 must reach each other. The iBGP sessions, this time, must be in
    #    full mesh configuration. AS3 will have only one eBGP peering with AS1 on the as1_s1 router.

    def build(self, *args, **kwargs):

        monde_ipv6 = "2001:2001"
        europe_ipv6 = monde_ipv6 + ":01"
        NA_ipv6 = monde_ipv6 + ":02"
        asia_ipv6 = monde_ipv6 + ":03"


        family = AF_INET6()
        # first step, adding routers
       
        # routers of MRS
        MRS1 = self.addRouter("MRS1", lo_addresses=[europe_ipv6 + "00:0001::/64"])
        MRS2 = self.addRouter("MRS2", lo_addresses=[europe_ipv6 + "00:0002::/64"])
         #routers of PAR
        PAR1 = self.addRouter("PAR1", lo_addresses=[europe_ipv6 + "01:0001::/64"])
        PAR2 = self.addRouter("PAR2", lo_addresses=[europe_ipv6 + "01:0002::/64"])
        # routers of SIN
        SIN1 = self.addRouter("SIN1", lo_addresses=[asie_ipv6 + "00:0001::/64"])
        SIN2 = self.addRouter("SIN2", lo_addresses=[asia_ipv6 + "00:0002::/64"])
        # routers of SYD
        SYD1 = self.addRouter("SYD1", lo_addresses=[asie_ipv6 + "01:0001::/64"])
        SYD2 = self.addRouter("SYD2", lo_addresses=[asie_ipv6 + "01:0002::/64"])
        # routers of LAX
        LAX1 = self.addRouter("LAX1", lo_addresses=[NA_ipv6 + "00:0001::/64"])
        LAX2 = self.addRouter("LAX2", lo_addresses=[NA_ipv6 + "00:0001::/64"])
        # routers of SJO
        SJO1 = self.addRouter("SJO1", lo_addresses=[NA_ipv6 + "01:0001::/64"])
        SJO2 = self.addRouter("SJO2", lo_addresses=[NA_pv6 + "01:0002::/64"])
        #routers of ASH
        ASH1 = self.addRouter("ASH1", lo_addresses=[NA_ipv6 + "02:0001::/64"])
        ASH2 = self.addRouter("ASH2", lo_addresses=[NA_ipv6 + "02:0002::/64"])
        
        
        
        # adding OSPF6 as IGP
        MRS1.addDaemon(OSPF6)
        MRS2.addDaemon(OSPF6)

        SIN1.addDaemon(OSPF6)
        SIN2.addDaemon(OSPF6)

        SYD1.addDaemon(OSPF6)
        SYD2.addDaemon(OSPF6)

        LAX1.addDaemon(OSPF6)        
        LAX2.addDaemon(OSPF6)

        SJO1.addDaemon(OSPF6)
        SJO2.addDaemon(OSPF6)

        ASH1.addDaemon(OSPF6)
        ASH2.addDaemon(OSPF6)

        PAR1.addDaemon(OSPF6)
        PAR2.addDaemon(OSPF6)

        H1_SIN1 = self.addHost("H1_SIN1")
        H1_PAR1 = self.addHost("H1_PAR1")

        # adding links between the routers (and hosts)
        l_MRS1_MRS2 = self.addLink(MRS1, MRS2)
        l_MRS1_MRS2[MRS1].addParams(ip=(europe_ipv6 + "00:1201::/64"))
        l_MRS1_MRS2[MRS2].addParams(ip=(europe_ipv6 + "00:1202::/64"))

        l_SIN1_SIN2 = self.addLink(SIN1, SIN2)
        l_SIN1_SIN2[SIN1].addParams(ip=asia_ipv6 + "00:1201::/64")
        l_SIN1_SIN2[SIN1].addParams(ip=asia_ipv6 + "00:1202::/64")

        l_SYD1_SYD2 = self.addLink(SYD1, SYD2)
        l_SYD1_SYD2[SYD1] = addParams(ip=asia_ipv6 + "01:1201::/64")
        l_SYD1_SYD2[SYD1] = addParams(ip=asia_ipv6 + "01:1202::/64")

        l_PAR1_PAR2 = self.addLink(MRS1, MRS2)
        l_PAR1_PAR2[PAR1].addParams(ip=(europe_ipv6 + "00:1201::/64"))
        l_PAR1_PAR2[PAR2].addParams(ip=(europe_ipv6 + "00:1202::/64"))

        l_ASH1_ASH2 = self.addLink(ASH1, ASH2)
        l_ASH1_ASH2[ASH1].addParams(ip=(NA_ipv6 + "02:1201::/64"))
        l_ASH1_ASH2[ASH1].addParams(ip=(NA_ipv6 + "02:1202::/64"))

        l_LAX1_LAX2 = self.addLink(LAX1, LAX2)
        l_LAX1_LAX2[LAX1].addParams(ip=(NA_ipv6 + "00:1201::/64"))
        l_LAX1_LAX2[LAX2].addParams(ip=(NA_ipv6 + "00:1202::/64"))

        l_SJO1_SJ2 = self.addLink(SJO1, SJO2)
        l_SJO1_SJO2[SJO1].addParams(ip=(NA_ipv6 + "01:1201::/64"))
        l_SJO1_SJO2[SJO2].addParams(ip=(NA_ipv6 + "01:1202::/64"))

        l_MRS1_SIN1 = self.addLink(MRS1, SIN1)
        l_MRS1_SIN1[MRS1].addParams(ip=(europe_ipv6 + "00:1101::/64"))
        l_MRS1_SIN1[SIN1].addParams(ip=(europe_ipv6 + "00:1101::/64"))

        l_MRS2_SIN2 = self.addLink(MRS2, SIN2)
        l_MRS1_SIN1[MRS2].addParams(ip=(europe_ipv6 + "00:2202::/64"))
        l_MRS1_SIN1[SIN2].addParams(ip=(europe_ipv6 + "00:2202::/64"))

        l_SIN1_SYD1 = self.addLink(SIN1, SYD1)
        l_SIN1_SYD1[SIN1].addParams(ip=(asia_ipv6 + "00:1101::/64"))
        l_SIN1_SYD1[SYD1].addParams(ip=(asia_ipv6 + "01:1101::/64"))

        l_SIN2_SYD2 = self.addLink(SIN1, SYD1)
        l_SIN2_SYD2[SIN2].addParams(ip=(asia_ipv6 + "00:2202::/64"))
        l_SIN2_SYD2[SYD12.addParams(ip=(asia_ipv6 + "01:2202::/64"))

        l_ASH1_LAX1 = self.addLink(SIN1, SYD1)
        l_ASH1_LAX1[ASH1].addParams(ip=(asia_ipv6 + "00:1101::/64"))
        l_ASH1_LAX1[LAX1].addParams(ip=(asia_ipv6 + "02:1101::/64"))

        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=SimpleBGPTopo())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
