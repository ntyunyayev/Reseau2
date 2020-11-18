#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, OSPF, RouterConfig, AF_INET6, AF_INET, set_rr, ebgp_session, SHARE, IP6Tables, InputFilter, Deny, Allow, Rule, bgp_fullmesh, bgp_peering, ebgp_session
import hashlib


monde_ipv6 = "1627:6000:0000"
europe_ipv6 = monde_ipv6 + ":0"
NA_ipv6 = monde_ipv6 + ":1"
asia_ipv6 = monde_ipv6 + ":2"
server_ipv6 = monde_ipv6 + ":3"
server_ipv4 = "162.76.248."

MRS_ipv4 = "162.76.241."
PAR_ipv4 = "162.76.242."
SIN_ipv4 = "162.76.243."
SYD_ipv4 = "162.76.244."
LAX_ipv4 = "162.76.245."
SJO_ipv4 = "162.76.246."
ASH_ipv4 = "162.76.247."


VDF_ipv4 = "160.76.7."
EQX_ipv4 = "160.76.8."
NTT_ipv4 = "160.76.9."
VDF_ipv6 = "1627:6100:0000:0"
EQX_ipv6 = "1627:6200:0000:0"
NTT_ipv6 = "1627:6300:0000:0"

def createPassword(key):
    hash_object = hashlib.sha256(bytes(key, encoding='utf-8'))
    return hash_object.hexdigest()
    
secretKey = "Nu798SHkJ6MRwm69rZvu"
VDF_PW = createPassword("VDF"+secretKey)
EQX_PW = createPassword("EQX"+secretKey)
NTT_PW = createPassword("NTT"+secretKey)
SERVER_PW = createPassword("SER"+secretKey)
OSPF_PW_EU = "99cj8HyU2WTj2Gm"
OSPF_PW_AS = "7fv8G8J2mT2KvpF"
OSPF_PW_NA = "v5x6j4S8MBDrLk6"


class SimpleBGPTopo(IPTopo):
    
    def build(self, *args, **kwargs):

       
        # first step, adding routers
        #=========================================================
       
        # routers of MRS
        MRS1 = self.addRouter("MRS1",config=RouterConfig, lo_addresses=[europe_ipv6 + "000::/64", MRS_ipv4 + "100/32"])
        MRS2 = self.addRouter("MRS2",config=RouterConfig, lo_addresses=[europe_ipv6 + "100::/64", MRS_ipv4 + "110/32"])
         #routers of PAR
        PAR1 = self.addRouter("PAR1",config=RouterConfig, lo_addresses=[europe_ipv6 + "200::/64", PAR_ipv4 + "100/32"])
        PAR2 = self.addRouter("PAR2",config=RouterConfig, lo_addresses=[europe_ipv6 + "300::/64", PAR_ipv4 + "110/32"])
        # routers of SIN
        SIN1 = self.addRouter("SIN1",config=RouterConfig, lo_addresses=[asia_ipv6 + "000::/64", SIN_ipv4 + "100/32"])
        SIN2 = self.addRouter("SIN2",config=RouterConfig, lo_addresses=[asia_ipv6 + "100::/64", SIN_ipv4 + "110/32"])
        # routers of SYD
        SYD1 = self.addRouter("SYD1",config=RouterConfig, lo_addresses=[asia_ipv6 + "200::/64", SYD_ipv4 + "100/32"])
        SYD2 = self.addRouter("SYD2",config=RouterConfig, lo_addresses=[asia_ipv6 + "300::/64", SYD_ipv4 + "110/32"])
        # routers of LAX
        LAX1 = self.addRouter("LAX1",config=RouterConfig, lo_addresses=[NA_ipv6 + "000::/64", LAX_ipv4 + "100/32"])
        LAX2 = self.addRouter("LAX2",config=RouterConfig, lo_addresses=[NA_ipv6 + "100::/64", LAX_ipv4 + "110/32"])
        # routers of SJO
        SJO1 = self.addRouter("SJO1",config=RouterConfig, lo_addresses=[NA_ipv6 + "200::/64", SJO_ipv4 + "100/32"])
        SJO2 = self.addRouter("SJO2",config=RouterConfig, lo_addresses=[NA_ipv6 + "300::/64", SJO_ipv4 + "110/32"])
        #routers of ASH
        ASH1 = self.addRouter("ASH1",config=RouterConfig, lo_addresses=[NA_ipv6 + "400::/64", ASH_ipv4 + "100/32"])
        ASH2 = self.addRouter("ASH2", config=RouterConfig,lo_addresses=[NA_ipv6 + "500::/64", ASH_ipv4 + "110/32"])
        #routers peering vodafone
        VDFSIN1 = self.addRouter("VDFSIN1",config=RouterConfig, lo_addresses=[VDF_ipv6 + "000::/64", VDF_ipv4 + "100/32"])
        VDFSIN2 = self.addRouter("VDFSIN2",config=RouterConfig, lo_addresses=[VDF_ipv6 + "001::/64", VDF_ipv4 + "110/32"])
        VDFASH1 = self.addRouter("VDFASH1",config=RouterConfig, lo_addresses=[VDF_ipv6 + "002::/64", VDF_ipv4 + "120/32"])
        VDFPAR2 = self.addRouter("VDFPAR2",config=RouterConfig, lo_addresses=[VDF_ipv6 + "003::/64", VDF_ipv4 + "130/32"])
        #routers peering equinix
        EQXSIN1 = self.addRouter("EQXSIN1",config=RouterConfig, lo_addresses=[EQX_ipv6 + "000::/64", EQX_ipv4 + "100/32"])
        EQXSYD2 = self.addRouter("EQXSYD2",config=RouterConfig, lo_addresses=[EQX_ipv6 + "001::/64", EQX_ipv4 + "110/32"])
        #routers peering NTT
        NTTSYD1 = self.addRouter("NTTSYD1",config=RouterConfig, lo_addresses=[NTT_ipv6 + "000::/64", NTT_ipv4 + "100/32"])
        NTTSYD2 = self.addRouter("NTTSYD2",config=RouterConfig, lo_addresses=[NTT_ipv6 + "001::/64", NTT_ipv4 + "110/32"])

        
        
        
        # adding OSPF6 as IGP
        #=========================================================
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

        VDFSIN1.addDaemon(OSPF6)
        VDFSIN2.addDaemon(OSPF6)
        VDFASH1.addDaemon(OSPF6)
        VDFPAR2.addDaemon(OSPF6)

        EQXSIN1.addDaemon(OSPF6)
        EQXSYD2.addDaemon(OSPF6)

        NTTSYD1.addDaemon(OSPF6)
        NTTSYD2.addDaemon(OSPF6)
        

        # adding OSPF
        #=========================================================

        MRS1.addDaemon(OSPF)
        MRS2.addDaemon(OSPF)

        SIN1.addDaemon(OSPF)
        SIN2.addDaemon(OSPF)

        SYD1.addDaemon(OSPF)
        SYD2.addDaemon(OSPF)

        LAX1.addDaemon(OSPF)        
        LAX2.addDaemon(OSPF)

        SJO1.addDaemon(OSPF)
        SJO2.addDaemon(OSPF)

        ASH1.addDaemon(OSPF)
        ASH2.addDaemon(OSPF)

        PAR1.addDaemon(OSPF)
        PAR2.addDaemon(OSPF)

        VDFSIN1.addDaemon(OSPF)
        VDFSIN2.addDaemon(OSPF)
        VDFASH1.addDaemon(OSPF)
        VDFPAR2.addDaemon(OSPF)

        EQXSIN1.addDaemon(OSPF)
        EQXSYD2.addDaemon(OSPF)

        NTTSYD1.addDaemon(OSPF)
        NTTSYD2.addDaemon(OSPF)

        # adding BGP 
        #=========================================================
        MRS1.addDaemon(BGP,debug=("neighbor",))
        MRS2.addDaemon(BGP,debug=("neighbor",))

        SIN1.addDaemon(BGP,debug=("neighbor",))
        SIN2.addDaemon(BGP,debug=("neighbor",))

        SYD1.addDaemon(BGP,debug=("neighbor",))
        SYD2.addDaemon(BGP,debug=("neighbor",))

        LAX1.addDaemon(BGP,debug=("neighbor",))       
        LAX2.addDaemon(BGP,debug=("updates",))

        SJO1.addDaemon(BGP,debug=("updates",))
        SJO2.addDaemon(BGP,debug=("updates",))

        ASH1.addDaemon(BGP,debug=("updates",))
        ASH2.addDaemon(BGP,debug=("updates",))

        PAR1.addDaemon(BGP,debug=("updates",))
        PAR2.addDaemon(BGP,debug=("updates",))

        VDFSIN1.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected']),),debug=("updates",))
        VDFSIN2.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected']),),debug=("updates",))
        VDFASH1.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected']),),debug=("updates",))
        VDFPAR2.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected']),),debug=("updates",))

        EQXSIN1.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected']),),debug=("updates",))
        EQXSYD2.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected']),),debug=("updates",))
        
        NTTSYD1.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected']),),debug=("updates",))
        NTTSYD2.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected']),),debug=("updates",))
      
        # linkin twin datacenters
        #=========================================================
        l_MRS1_MRS2 = self.addLink(MRS1,MRS2,igp_metric=2,password = OSPF_PW_EU)
        l_MRS1_MRS2[MRS1].addParams(ip=(europe_ipv6 + "00a::1/64", MRS_ipv4 + "129/30"))
        l_MRS1_MRS2[MRS2].addParams(ip=(europe_ipv6 + "00a::2/64", MRS_ipv4 + "130/30"))

        l_SIN1_SIN2 = self.addLink(SIN1,SIN2,igp_metric=2,password = OSPF_PW_AS)
        l_SIN1_SIN2[SIN1].addParams(ip=(asia_ipv6 + "00a::1/64", SIN_ipv4 + "129/30"))
        l_SIN1_SIN2[SIN2].addParams(ip=(asia_ipv6 + "00a::2/64", SIN_ipv4 + "130/30"))

        l_SYD1_SYD2 = self.addLink(SYD1,SYD2,igp_metric=2,password = OSPF_PW_AS)
        l_SYD1_SYD2[SYD1].addParams(ip=(asia_ipv6 + "00c::1/64", SYD_ipv4 + "129/30"))
        l_SYD1_SYD2[SYD2].addParams(ip=(asia_ipv6 + "00c::2/64", SYD_ipv4 + "130/30"))

        l_PAR1_PAR2 = self.addLink(PAR1,PAR2,igp_metric=2,password = OSPF_PW_EU)
        l_PAR1_PAR2[PAR1].addParams(ip=(europe_ipv6 + "00b::1/64", PAR_ipv4 + "129/30"))
        l_PAR1_PAR2[PAR2].addParams(ip=(europe_ipv6 + "00b::2/64", PAR_ipv4 + "130/30"))

        l_ASH1_ASH2 = self.addLink(ASH1, ASH2,igp_metric=2,password = OSPF_PW_NA)
        l_ASH1_ASH2[ASH1].addParams(ip=(NA_ipv6 + "00a::1/64", ASH_ipv4 + "129/30"))
        l_ASH1_ASH2[ASH2].addParams(ip=(NA_ipv6 + "00a::2/64", ASH_ipv4 + "130/30"))

        l_LAX1_LAX2 = self.addLink(LAX1, LAX2,igp_metric=2,password = OSPF_PW_NA)
        l_LAX1_LAX2[LAX1].addParams(ip=(NA_ipv6 + "00b::1/64", LAX_ipv4 + "129/30"))
        l_LAX1_LAX2[LAX2].addParams(ip=(NA_ipv6 + "00b::2/64", LAX_ipv4 + "130/30"))

        l_SJO1_SJO2 = self.addLink(SJO1, SJO2,igp_metric=2,password = OSPF_PW_NA)
        l_SJO1_SJO2[SJO1].addParams(ip=(NA_ipv6 + "00c::1/64", SJO_ipv4 + "129/30"))
        l_SJO1_SJO2[SJO2].addParams(ip=(NA_ipv6 + "00c::2/64", SJO_ipv4 + "130/30"))

        #=========================================================

        l_MRS1_SIN1 = self.addLink(MRS1, SIN1,igp_metric=11,password = OSPF_PW_EU)
        l_MRS1_SIN1[MRS1].addParams(ip=(europe_ipv6 + "011::1/64", MRS_ipv4 + "5/30"))
        l_MRS1_SIN1[SIN1].addParams(ip=(europe_ipv6 + "011::2/64", MRS_ipv4 + "6/30"))

        l_MRS2_SIN2 = self.addLink(MRS2, SIN2,igp_metric=11,password = OSPF_PW_EU)
        l_MRS2_SIN2[MRS2].addParams(ip=(europe_ipv6 + "022::1/64", MRS_ipv4 + "9/30"))
        l_MRS2_SIN2[SIN2].addParams(ip=(europe_ipv6 + "022::2/64", MRS_ipv4 + "10/30"))

        l_SIN1_SYD1 = self.addLink(SIN1, SYD1,igp_metric=3,password = OSPF_PW_AS)
        l_SIN1_SYD1[SIN1].addParams(ip=(asia_ipv6 + "011::1/64", SIN_ipv4 + "5/30"))
        l_SIN1_SYD1[SYD1].addParams(ip=(asia_ipv6 + "011::2/64", SIN_ipv4 + "6/30"))

        l_SIN2_SYD2 = self.addLink(SIN2, SYD2,igp_metric=3,password = OSPF_PW_AS)
        l_SIN2_SYD2[SIN2].addParams(ip=(asia_ipv6 + "022::1/64", SIN_ipv4 + "9/30"))
        l_SIN2_SYD2[SYD2].addParams(ip=(asia_ipv6 + "022::2/64", SIN_ipv4 + "10/30"))

        l_SIN2_SJO1 = self.addLink(SIN2, SJO1,igp_metric=11,password = OSPF_PW_AS)
        l_SIN2_SJO1[SIN2].addParams(ip=(asia_ipv6 + "021::1/64", SIN_ipv4 + "13/30"))
        l_SIN2_SJO1[SJO1].addParams(ip=(asia_ipv6 + "021::2/64", SIN_ipv4 + "14/30"))

        l_SIN1_SJO2 = self.addLink(SIN1, SJO2,igp_metric=11,password = OSPF_PW_AS)
        l_SIN1_SJO2[SIN1].addParams(ip=(asia_ipv6 + "220::1/64", SIN_ipv4 + "17/30"))
        l_SIN1_SJO2[SJO2].addParams(ip=(asia_ipv6 + "220::2/64", SIN_ipv4 + "18/30"))

        #=======================================================


        l_ASH1_LAX1 = self.addLink(ASH1, LAX1,igp_metric=3,password = OSPF_PW_NA)
        l_ASH1_LAX1[ASH1].addParams(ip=(NA_ipv6 + "011::1/64", ASH_ipv4 + "5/30"))
        l_ASH1_LAX1[LAX1].addParams(ip=(NA_ipv6 + "011::2/64", ASH_ipv4 + "6/30"))

        l_ASH2_LAX2 = self.addLink(ASH2, LAX2,igp_metric=3,password = OSPF_PW_NA)
        l_ASH2_LAX2[ASH2].addParams(ip=(NA_ipv6 + "022::1/64", ASH_ipv4 + "9/30"))
        l_ASH2_LAX2[LAX2].addParams(ip=(NA_ipv6 + "022::2/64", ASH_ipv4 + "10/30"))

        l_ASH1_LAX2 = self.addLink(ASH1, LAX2,igp_metric=3,password = OSPF_PW_NA)
        l_ASH1_LAX2[ASH1].addParams(ip=(NA_ipv6 + "012::1/64", ASH_ipv4 + "13/30"))
        l_ASH1_LAX2[LAX2].addParams(ip=(NA_ipv6 + "012::2/64", ASH_ipv4 + "14/30"))

        l_SJO1_LAX1 = self.addLink(SJO1, LAX1,igp_metric=3,password = OSPF_PW_NA)
        l_SJO1_LAX1[SJO1].addParams(ip=(NA_ipv6 + "110::1/64", SJO_ipv4 + "5/30"))
        l_SJO1_LAX1[LAX1].addParams(ip=(NA_ipv6 + "110::2/64", SJO_ipv4 + "6/30"))

        l_SJO2_LAX2 = self.addLink(SJO2,LAX2,igp_metric=3,password = OSPF_PW_NA)
        l_SJO2_LAX2[SJO2].addParams(ip=(NA_ipv6 + "220::1/64", SJO_ipv4 + "9/30"))
        l_SJO2_LAX2[LAX2].addParams(ip=(NA_ipv6 + "220::2/64", SJO_ipv4 + "10/30"))

        l_PAR1_ASH1 = self.addLink(PAR1,ASH1, igp_metric=11,password = OSPF_PW_EU)
        l_PAR1_ASH1[PAR1].addParams(ip=(europe_ipv6 + "110::1/64", PAR_ipv4 + "5/30"))
        l_PAR1_ASH1[ASH1].addParams(ip=(europe_ipv6 + "110::2/64", PAR_ipv4 + "6/30"))

        l_PAR2_ASH2 = self.addLink(PAR2,ASH2,igp_metric=11,password = OSPF_PW_EU)
        l_PAR2_ASH2[PAR2].addParams(ip=(europe_ipv6 + "220::1/64", PAR_ipv4 + "9/30"))
        l_PAR2_ASH2[ASH2].addParams(ip=(europe_ipv6 + "220::2/64", PAR_ipv4 + "10/30"))

        l_PAR1_MRS2 = self.addLink(PAR1,MRS2,igp_metric=3,password = OSPF_PW_EU)
        l_PAR1_MRS2[PAR1].addParams(ip=(europe_ipv6 + "101::1/64", PAR_ipv4 + "13/30"))
        l_PAR1_MRS2[MRS2].addParams(ip=(europe_ipv6 + "101::2/64", PAR_ipv4 + "14/30"))

        l_PAR2_MRS1 = self.addLink(PAR2, MRS1,igp_metric=3,password = OSPF_PW_EU)
        l_PAR2_MRS1[PAR2].addParams(ip=(europe_ipv6 + "202::1/64", PAR_ipv4 + "17/30"))
        l_PAR2_MRS1[MRS1].addParams(ip=(europe_ipv6 + "202::2/64", PAR_ipv4 + "18/30"))

        l_SYD2_LAX2 = self.addLink(SYD2,LAX2,igp_metric=11,password = OSPF_PW_AS)
        l_SYD2_LAX2[SYD2].addParams(ip=(europe_ipv6 + "303::1/64", SYD_ipv4 + "5/30"))
        l_SYD2_LAX2[LAX2].addParams(ip=(europe_ipv6 + "303::2/64", SYD_ipv4 + "6/30"))

        #=============================================================================
        #Peering links

        l_VDF_PAR2 = self.addLink(VDFPAR2, PAR2,igp_metric=11)
        l_VDF_PAR2[VDFPAR2].addParams(ip=(europe_ipv6 + "ffa::1/64",PAR_ipv4 + "21/30"))
        l_VDF_PAR2[PAR2].addParams(ip=(europe_ipv6 + "ffa::2/64",PAR_ipv4 + "22/30"))

        l_VDF_ASH1 = self.addLink(VDFASH1,ASH1,igp_metric=11)
        l_VDF_ASH1[VDFASH1].addParams(ip=(NA_ipv6 + "ffa::1/64",ASH_ipv4 + "21/30"))
        l_VDF_ASH1[ASH1].addParams(ip=(NA_ipv6 + "ffa::2/64",ASH_ipv4 + "22/30"))

        l_VDF_SIN1 = self.addLink(VDFSIN1, SIN1,igp_metric=11)
        l_VDF_SIN1[VDFSIN1].addParams(ip=(asia_ipv6 + "ffa::1/64",SIN_ipv4 + "21/30"))
        l_VDF_SIN1[SIN1].addParams(ip=(asia_ipv6 + "ffa::2/64",SIN_ipv4 + "22/30"))

        l_VDF_SIN2 = self.addLink(VDFSIN2, SIN2,igp_metric=11)
        l_VDF_SIN2[VDFSIN2].addParams(ip=(asia_ipv6 + "1fa::1/64",SIN_ipv4 + "25/30"))
        l_VDF_SIN2[SIN2].addParams(ip=(asia_ipv6 + "1fa::2/64",SIN_ipv4 + "26/30"))

        l_EQX_SIN1 = self.addLink(EQXSIN1, SIN1,igp_metric=11)
        l_EQX_SIN1[EQXSIN1].addParams(ip=(asia_ipv6 + "2fb::1/64",SIN_ipv4 + "29/30"))
        l_EQX_SIN1[SIN1].addParams(ip=(asia_ipv6 + "2fb::2/64",SIN_ipv4 + "30/30"))

        l_EQX_SYD2 = self.addLink(EQXSYD2, SYD2,igp_metric=11)
        l_EQX_SYD2[EQXSYD2].addParams(ip=(asia_ipv6 + "3fa::1/64",SYD_ipv4 + "9/30"))
        l_EQX_SYD2[SYD2].addParams(ip=(asia_ipv6 + "3fa::2/64",SYD_ipv4 + "10/30"))

        l_NTT_SYD2 = self.addLink(NTTSYD2, SYD2,igp_metric=11)
        l_NTT_SYD2[NTTSYD2].addParams(ip=(asia_ipv6 + "4fb::1/64",SYD_ipv4 + "13/30"))
        l_NTT_SYD2[SYD2].addParams(ip=(asia_ipv6 + "4fb::2/64",SYD_ipv4 + "14/30"))

        l_NTT_SYD1 = self.addLink(NTTSYD1, SYD1,igp_metric=11)
        l_NTT_SYD1[NTTSYD1].addParams(ip=(asia_ipv6 + "5fa::1/64",SYD_ipv4 + "17/30"))
        l_NTT_SYD1[SYD1].addParams(ip=(asia_ipv6 + "5fa::2/64",SYD_ipv4 + "18/30"))


        #=============================================================================
        #servers

        S1 = self.addRouter("S1", config=RouterConfig, lo_addresses=[server_ipv6 + "::/64", server_ipv4 + "1/32"])
        S2 = self.addRouter("S2", config=RouterConfig, lo_addresses=[server_ipv6 + "::/64", server_ipv4 + "1/32"])

        #Adding BGP daemons to manage failures

        S1.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected'])))
        S2.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected'])))

        # S1.addDaemon(OSPF6)
        # S2.addDaemon(OSPF6)
        
        self.addAS(64512, (S1,))
        self.addAS(64512, (S2,))

        l_S1_SJO2 = self.addLink(S1,SJO2, igp_metric=3)
        l_S1_SJO2[S1].addParams(ip=(server_ipv6 + "a1a::1/64",server_ipv4 + "5/30"))
        l_S1_SJO2[SJO2].addParams(ip=(server_ipv6 + "a1a::2/64",server_ipv4 + "6/30"))

        l_S2_PAR2 = self.addLink(S2,PAR2, igp_metric=3)
        l_S2_PAR2[S2].addParams(ip=(server_ipv6 + "a1a::3/64",server_ipv4 + "9/30"))
        l_S2_PAR2[PAR2].addParams(ip=(server_ipv6 + "a1a::4/64",server_ipv4 + "10/30"))

        ebgp_session(self,S1, SJO2)
        ebgp_session(self,S2, PAR2)
        

        #=============================================================================
        # BGP setup
        self.addAS(1,(MRS1,MRS2,PAR1,PAR2,SIN1,SIN2,SYD1,SYD2,SJO1,SJO2,LAX1,LAX2,ASH1,ASH2))
        set_rr(self, rr=SIN1, peers=[SYD1, MRS1, SIN2, MRS2, SJO1, SJO2, SYD2, ASH1, PAR2, SJO1])
        set_rr(self, rr=SYD2, peers=[SYD1, SIN2, LAX1, LAX2, SIN1, ASH1, PAR2, SJO1])
        set_rr(self, rr=ASH1, peers=[SJO1, SJO2, LAX1, LAX2, PAR1, ASH2, SIN1,SYD2, PAR2, SJO1])
        set_rr(self, rr=PAR2, peers=[MRS1, MRS2, PAR1, ASH2, SIN1, SYD2, ASH1, SJO1])
        set_rr(self, rr=SJO1, peers=[SYD2, PAR2, SIN1, ASH1])
        # bgp_fullmesh(self, [MRS1,MRS2,PAR1,PAR2,SIN1,SIN2,SYD1,SYD2,SJO1,SJO2,LAX1,LAX2,ASH1,ASH2])
       
        self.addAS(2, (EQXSIN1,EQXSYD2))
        self.addAS(3, (VDFASH1,VDFPAR2,VDFSIN1,VDFSIN2))
        self.addAS(4, (NTTSYD1,NTTSYD2))

        ebgp_session(self, VDFPAR2, PAR2)
        ebgp_session(self, VDFASH1, ASH1)
        ebgp_session(self, VDFSIN1, SIN1)
        ebgp_session(self, VDFSIN2, SIN2)
        ebgp_session(self, EQXSIN1, SIN1)
        ebgp_session(self, EQXSYD2, SYD2)
        ebgp_session(self, NTTSYD2, SYD2)
        ebgp_session(self, NTTSYD1, SYD1)


        hVdfPar2 = self.addHost("hVdfPar2")
        hVdfAsh1 = self.addHost("hVdfAsh1")
        hVdfSin1 = self.addHost("hVdfSin1")
        hVdfSin2 = self.addHost("hVdfSin2")

        hEqxSin1 = self.addHost("hEqxSin1")
        hEqxSyd2 = self.addHost("hEqxSyd2")

        hNttSyd2 = self.addHost("hNttSyd2")
        hNttSyd1 = self.addHost("hNttSyd1")
        


        l_hVdfPar2 = self.addLink(hVdfPar2, VDFPAR2,igp_metric=2)
        l_hVdfPar2[hVdfPar2].addParams(ip=(VDF_ipv6 + "aaa::1/64", VDF_ipv4 + "21/30"))
        l_hVdfPar2[VDFPAR2].addParams(ip=(VDF_ipv6 + "aaa::2/64", VDF_ipv4 + "22/30"))

        l_hVdfAsh1 = self.addLink(hVdfAsh1, VDFASH1,igp_metric=2)
        l_hVdfAsh1[hVdfAsh1].addParams(ip=(VDF_ipv6 + "bbb::1/64", VDF_ipv4 + "25/30"))
        l_hVdfAsh1[VDFASH1].addParams(ip=(VDF_ipv6 + "bbb::2/64", VDF_ipv4 + "26/30"))

        l_hVdfSin1 = self.addLink(hVdfSin1, VDFSIN1,igp_metric=2)
        l_hVdfSin1[hVdfSin1].addParams(ip=(VDF_ipv6 + "ccc::1/64", VDF_ipv4 + "29/30"))
        l_hVdfSin1[VDFSIN1].addParams(ip=(VDF_ipv6 + "ccc::2/64", VDF_ipv4 + "30/30"))

        l_hVdfSin2 = self.addLink(hVdfSin2, VDFSIN2,igp_metric=2)
        l_hVdfSin2[hVdfSin2].addParams(ip=(VDF_ipv6 + "ddd::1/64", VDF_ipv4 + "33/30"))
        l_hVdfSin2[VDFSIN2].addParams(ip=(VDF_ipv6 + "ddd::2/64", VDF_ipv4 + "34/30"))

        l_hEqxSyd2 = self.addLink(hEqxSyd2, EQXSYD2,igp_metric=2)
        l_hEqxSyd2[hEqxSyd2].addParams(ip=(EQX_ipv6 + "aaa::1/64", EQX_ipv4 + "13/30"))
        l_hEqxSyd2[EQXSYD2].addParams(ip=(EQX_ipv6 + "aaa::2/64", EQX_ipv4 + "14/30"))

        l_hEqxSin1 = self.addLink(hEqxSin1, EQXSIN1,igp_metric=2)
        l_hEqxSin1[hEqxSin1].addParams(ip=(EQX_ipv6 + "bbb::1/64", EQX_ipv4 + "17/30"))
        l_hEqxSin1[EQXSIN1].addParams(ip=(EQX_ipv6 + "bbb::2/64", EQX_ipv4 + "18/30"))

        l_hNttSyd2 = self.addLink(hNttSyd2, NTTSYD2,igp_metric=2)
        l_hNttSyd2[hNttSyd2].addParams(ip=(NTT_ipv6 + "aaa::1/64", NTT_ipv4 + "13/30"))
        l_hNttSyd2[NTTSYD2].addParams(ip=(NTT_ipv6 + "aaa::2/64", NTT_ipv4 + "14/30"))

        l_hNttSyd1= self.addLink(hNttSyd1, NTTSYD1,igp_metric=2)
        l_hNttSyd1[hNttSyd1].addParams(ip=(NTT_ipv6 + "bbb::1/64", NTT_ipv4 + "17/30"))
        l_hNttSyd1[NTTSYD1].addParams(ip=(NTT_ipv6 + "bbb::2/64", NTT_ipv4 + "18/30"))


        #=============================================================================
        #communities set up


        super().build(*args, **kwargs)

# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=SimpleBGPTopo(), allocate_IPs=False)
    try:
        net.start()
        ########################################

        #Defining communities
        community_as_prepend_x1 = "1:100"
        community_as_prepend_x1_name = "prepend_x1"
        community_as_prepend_x2 = "2:100"
        community_as_prepend_x2_name = "prepend_x2"
        community_local_pref_200 = "200:200"
        community_local_pref_200_name = "local_pref_200"
        general_route_map = "general_route_map"

        #Reducing Timeout to give better response to failures for servers
        print(net['PAR2'].cmd('python3 scripts/BGP_V6_KALIVE_TIMEOUT.py {} {} {}'.format("1627:6000:0:3a1a::3",1,4)))
        print(net['S2'].cmd('python3 scripts/BGP_V6_KALIVE_TIMEOUT.py {} {} {}'.format("1627:6000:0:3a1a::4",1,4)))
        print(net['SJO2'].cmd('python3 scripts/BGP_V6_KALIVE_TIMEOUT.py {} {} {}'.format("1627:6000:0:3a1a::1",1,4)))
        print(net['S1'].cmd('python3 scripts/BGP_V6_KALIVE_TIMEOUT.py {} {} {}'.format("1627:6000:0:3a1a::2",1,4)))

        #Removing private AS from AS-PATH
        print(net['PAR2'].cmd('python3 scripts/BGP_rm_aspath_ASN_RM_SEQ.py {} {} {}'.format(64512,general_route_map,10)))
        print(net['SJO2'].cmd('python3 scripts/BGP_rm_aspath_ASN_RM_SEQ.py {} {} {}'.format(64512,general_route_map,10)))
        print(net['PAR2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format("1627:6000:0:3a1a::3",general_route_map,"in")))
        print(net['SJO2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format("1627:6000:0:3a1a::1",general_route_map,"in")))
    
        # Configuring TTL and PASSWORD for PAR1-S2
        # print(net['PAR1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format("1627:6000:0:3a1a::3",2,SERVER_PW)))
        # print(net['S2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format("1627:6000:0:3a1a::4",2,SERVER_PW)))
        
        # #Configuring TTL and PASSWORD for SIN1-EQX
        # # print(net['EQX'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "2fb::2",2,EQX_PW)))
        # # print(net['SIN1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "2fb::1",2,EQX_PW)))

        # # #Configuring TTL and PASSWORD for SYD2-NTT
        # # print(net['NTT'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "4fb::2",2,NTT_PW)))
        # # print(net['SYD2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "4fb::1",2,NTT_PW)))

        # # #Configuring TTL and PASSWORD for PAR2-VDF
        # # print(net['VDF'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(europe_ipv6 + "ffa::2",2,VDF_PW)))
        # # print(net['PAR2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(europe_ipv6 + "ffa::1",2,VDF_PW)))
        # ########################################

        #Configuring TTL and PASSWORD for S2
        # print(net['PAR1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format("1627:6000:0:3a1a::3",2,SERVER_PW)))
        # print(net['S2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format("1627:6000:0:3a1a::4",2,SERVER_PW)))
        
        # #Configuring TTL and PASSWORD for EQX
        # print(net['EQXSIN1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "2fb::2",2,EQX_PW)))
        # print(net['SIN1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "2fb::1",2,EQX_PW)))

        # print(net['EQXSYD2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "3fa::2",2,EQX_PW)))
        # print(net['SYD2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "3fa::1",2,EQX_PW)))

        # #Configuring TTL and PASSWORD for NTT
        # print(net['NTTSYD2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "4fb::2",2,NTT_PW)))
        # print(net['SYD2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {print(net['VDFPAR2'].cmd('python3 scripts/BGP_SET_ANY_COMM_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1,general_route_map,10)))
        # print(net['VDFPAR2'].cmd('python3 scripts/BGP_SET_ANY_COMM_RMNAME_SEQ.py {} {} {}'.format(community_local_pref_200,general_route_map,30)))
        # print(net['VDFPAR2'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
        # print(net['VDFPAR2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(europe_ipv6 + "ffa::2",general_route_map,"out")))} {} {}'.format(asia_ipv6 + "4fb::1",2,NTT_PW)))

        # print(net['NTTSYD1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "5fa::2",2,NTT_PW)))
        # print(net['SYD1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "5fa::1",2,NTT_PW)))
        
        # #Configuring TTL and PASSWORD for VDF
        # print(net['VDFPAR2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(europe_ipv6 + "ffa::2",2,VDF_PW)))
        # print(net['PAR2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(europe_ipv6 + "ffa::1",2,VDF_PW)))

        # print(net['VDFASH1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(NA_ipv6 + "ffa::2",2,VDF_PW)))
        # print(net['ASH1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(NA_ipv6 + "ffa::1",2,VDF_PW)))

        # print(net['VDFSIN1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "ffa::2",2,VDF_PW)))
        # print(net['SIN1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "ffa::1",2,VDF_PW)))

        # print(net['VDFSIN2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(europe_ipv6 + "1fa::2",2,VDF_PW)))
        # print(net['SIN2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(europe_ipv6 + "1fa::1",2,VDF_PW)))

        # ########################################
        ##########################################
        ##START TAG COMMUNITY
        #creating community lists
        print(net['SIN1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
        print(net['SIN1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x2,community_as_prepend_x2_name)))
        print(net['SIN1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
        #Adding prepend X1
        print(net['SIN1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,10)))
        #Adding prepend X2
        print(net['SIN1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x2_name,general_route_map,20)))
        #Adding local-pref 200
        print(net['SIN1'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name, 200, general_route_map,30)))
        #Adding default permit at the end
        print(net['SIN1'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
        #applying route-map on neighbors
        print(net['SIN1'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(asia_ipv6 + "2fb::1",general_route_map,"in")))
        print(net['SIN1'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(asia_ipv6 + "ffa::1",general_route_map,"in")))

        #=================================#
        #=================================#

        print(net['SIN2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
        print(net['SIN2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x2,community_as_prepend_x2_name)))
        print(net['SIN2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
        #Adding prepend X1
        print(net['SIN2'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,10)))
        #Adding prepend X2
        print(net['SIN2'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x2_name,general_route_map,20)))
        #Adding local-pref 200
        print(net['SIN2'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name, 200, general_route_map,30)))
        #Adding default permit at the end
        print(net['SIN2'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
        #applying route-map on neighbors
        print(net['SIN2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(asia_ipv6 + "1fa::1",general_route_map,"in")))

        # #=================================#
        # #=================================#
        
        print(net['SYD1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
        print(net['SYD1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x2,community_as_prepend_x2_name)))
        print(net['SYD1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
        #Adding prepend X1
        print(net['SYD1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,10)))
        #Adding prepend X2
        print(net['SYD1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x2_name,general_route_map,20)))
        #Adding local-pref 200
        print(net['SYD1'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name, 200, general_route_map,30)))
        #Adding default permit at the end
        print(net['SYD1'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
        #applying route-map on neighbors
        print(net['SYD1'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(asia_ipv6 + "5fa::1",general_route_map,"in")))

        # #=================================#
        # #=================================#

        print(net['SYD2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
        print(net['SYD2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x2,community_as_prepend_x2_name)))
        print(net['SYD2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
        #Adding prepend X1
        print(net['SYD2'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,10)))
        #Adding prepend X2
        print(net['SYD2'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x2_name,general_route_map,20)))
        #Adding local-pref 200
        print(net['SYD2'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name, 200, general_route_map,30)))
        #Adding default permit at the end
        print(net['SYD2'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
        #applying route-map on neighbors
        print(net['SYD2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(asia_ipv6 + "3fa::1",general_route_map,"in")))
        print(net['SYD2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(asia_ipv6 + "4fb::1",general_route_map,"in")))

        # #=================================#
        # #=================================#
    
        print(net['ASH1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
        print(net['ASH1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x2,community_as_prepend_x2_name)))
        print(net['ASH1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
        #Adding prepend X1
        print(net['ASH1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,10)))
        #Adding prepend X2
        print(net['ASH1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x2_name,general_route_map,20)))
        #Adding local-pref 200
        print(net['ASH1'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name, 200, general_route_map,30)))
        #Adding default permit at the end
        print(net['ASH1'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
        #applying route-map on neighbors
        print(net['ASH1'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(NA_ipv6 + "ffa::1",general_route_map,"in")))

        # #=================================#
        # #=================================#
    
        print(net['PAR2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
        print(net['PAR2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x2,community_as_prepend_x2_name)))
        print(net['PAR2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
        #Adding prepend X1
        print(net['PAR2'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,10)))
        #Adding prepend X2
        print(net['PAR2'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x2_name,general_route_map,20)))
        #Adding local-pref 200
        print(net['PAR2'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name, 200, general_route_map,30)))
        #Adding default permit at the end
        print(net['PAR2'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
        #applying route-map on neighbors
        print(net['PAR2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(europe_ipv6 + "ffa::1",general_route_map,"in")))

        ###END TAG COMMUNITY
        #=================================#
        #=================================#

        ###TESTING COMMUNITIES#############
        # print(net['VDFPAR2'].cmd('python3 scripts/BGP_SET_ANY_COMM_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1,general_route_map,10)))
        # print(net['VDFPAR2'].cmd('python3 scripts/BGP_SET_ANY_COMM_RMNAME_SEQ.py {} {} {}'.format(community_local_pref_200,general_route_map,30)))
        # print(net['VDFPAR2'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
        # print(net['VDFPAR2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(europe_ipv6 + "ffa::2",general_route_map,"out")))

        IPCLI(net)
    finally:
        net.stop()
