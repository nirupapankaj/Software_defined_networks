#!/usr/bin/python

"""
Script created by VND - Visual Network Description (SDN version)
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, IVSSwitch, UserSwitch
from mininet.link import Link, TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def topology():
    "Create a network."

    print "*** Creating nodes"
    net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )

    print "*** Creating nodes"
    h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8' )
    h2 = net.addHost( 'h2', mac='00:00:00:00:00:02', ip='10.0.0.2/8' )
    h3 = net.addHost( 'h3', mac='00:00:00:00:00:03', ip='10.0.0.3/8' )
    h4 = net.addHost( 'h4', mac='00:00:00:00:00:04', ip='10.0.0.4/8' )
    s5 = net.addSwitch( 's5', listenPort=6673, mac='00:00:00:00:00:05' )
    s6 = net.addSwitch( 's6', listenPort=6674, mac='00:00:00:00:00:06' )
    s7 = net.addSwitch( 's7', listenPort=6675, mac='00:00:00:00:00:07' )
    c8 = net.addController( 'c8', controller=RemoteController, ip='192.168.56.3', port=6653 )

    print "*** Creating links"
    net.addLink(s6, s7, 3, 2, bw=10)
    net.addLink(s5, s7, 3, 1, bw=10)
    net.addLink(h4, s6, 0, 2, bw=10)
    net.addLink(h3, s6, 0, 1, bw=10)
    net.addLink(h2, s5, 0, 2, bw=10)
    net.addLink(h1, s5, 0, 1, bw=10)

    print "*** Starting network"
    net.build()
    c8.start()
    s5.start( [c8] )
    s6.start( [c8] )
    s7.start( [c8] )

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
