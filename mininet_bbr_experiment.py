from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
import os

def setup_network():
    # Create a Mininet instance
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSSwitch)

    # Add hosts
    client1 = net.addHost('client1', ip='192.168.254.11/24')
    client2 = net.addHost('client2', ip='192.168.254.31/24')
    server1 = net.addHost('server1', ip='192.168.253.11/24')
    server2 = net.addHost('server2', ip='192.168.253.31/24')
    
    # Add a router node
    router = net.addHost('router')

    #create two bridge on the router
    router.cmd('brctl addbr br_clients')
    router.cmd('brctl addbr br_servers')

    #Bring up the bridges
    router.cmd('ip link set br_clients up')
    router.cmd('ip link set br_servers up')

    # Add links with updated TC parameters
    net.addLink(server1, router, intfName2='router-eth1', bw=1000)
    net.addLink(server2, router, intfName2='router-eth2', bw=1000)
    net.addLink(client1, router, intfName2='router-eth3', bw=1000)
    net.addLink(client2, router, intfName2='router-eth4', bw=1000)

    #Attach client interfaces to br_clients
    router.cmd('brctl addif br_clients router-eth3')
    router.cmd('brctl addif br_clients router-eth4')

    #Attach server interfaces to br_servers
    router.cmd('brctl addif br_servers router-eth1')
    router.cmd('brctl addif br_servers router-eth2')

    router.cmd('ip addr add 192.168.254.6/24 dev br_clients')
    router.cmd('ip addr add 192.168.253.5/24 dev br_servers')
    router.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Start the network
    net.start()

    # Apply additional TC rules to router interfaces
    router.cmd('sudo tc qdisc add dev br_clients root netem delay 10ms rate 1000mbit')
    router.cmd('sudo tc qdisc add dev br_clients parent 1:1 handle 10: tbf rate 1000mbit burst 100kb')
    router.cmd('sudo tc qdisc add dev br_servers root netem delay 10ms rate 1000mbit')
    router.cmd('sudo tc qdisc add dev br_servers parent 1:1 handle 10: tbf rate 1000mbit burst 100kb')
    
    #Add default route on the clients and the servers
    client1.setDefaultRoute('via 192.168.254.6')
    client2.setDefaultRoute('via 192.168.254.6')
    server1.setDefaultRoute('via 192.168.253.5')
    server2.setDefaultRoute('via 192.168.253.5')
   

    client1.cmd('sysctl -w net.ipv4.tcp_congestion_control=bbr')
    server1.cmd('sysctl -w net.ipv4.tcp_congestion_control=bbr')
    # Run iperf-reliable on client connecting to both servers using IP addresses
    client1.cmd("~/iperf-reliable/src/iperf3 -s -F /dev/null -d -r > client1.log 2>&1 &")
    client2.cmd("~/iperf-reliable/src/iperf3 -s -F /dev/null -d -r > client2.log 2>&1 &")

    # Run iperf-reliable on server1 and server2
    server1.cmd("~/iperf-reliable/src/iperf3 -t 100 -c 192.168.254.11 -F /dev/random > server1.log 2>&1 &")
    server2.cmd("~/iperf-reliable/src/iperf3 -t 100 -c 192.168.254.31 -F /dev/random > server2.log")

    # Launch the CLI for interactive commands
    CLI(net)

    # Stop the network after exiting CLI
    net.stop()

if __name__ == '__main__':
    setup_network()

